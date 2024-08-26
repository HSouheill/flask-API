import openai
import os
from flask import Flask, request, jsonify
from functools import wraps
from flask_cors import CORS
import base64
import requests

app = Flask(__name__)

CORS(app)
openai.api_key = os.getenv("OPENAI_API_KEY")

def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        if api_key != os.getenv("API_KEY"):
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return wrapper

@app.route('/', methods=['GET'])
@authenticate
def index():
    return jsonify({'response': 'Hello, World!'})

@app.route('/chat', methods=['POST'])
@authenticate
def chat():
    data = request.get_json()

    if 'content' not in data:
        return jsonify({'error': 'Invalid input, "content" is required'}), 400

    user_message = data['content']

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        assistant_message = response['choices'][0]['message']['content'].strip()

        return jsonify({
            'response': assistant_message,
            'version': '0.1.0'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/generateImage', methods=['POST'])
@authenticate
def generate_image():
    data = request.get_json()
    if 'content' not in data:
        return jsonify({'error': 'Invalid input, "content" is required'}), 400

    user_message = data['content']
    response_type = request.headers.get('response-type', 'image') 

    try:
        image_response = openai.Image.create(
            prompt=user_message,
            n=1,
            size="1024x1024"
        )

        image_url = image_response['data'][0]['url']

        if response_type == 'base64':
            image_data = requests.get(image_url).content
            base64_image = base64.b64encode(image_data).decode('utf-8')

            return jsonify({
                'base64': base64_image,
                'version': '0.1.0'
            })

        return jsonify({
            'image_url': image_url,
            'version': '0.1.0'
        })

    except openai.error.OpenAIError as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
