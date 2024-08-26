import unittest
from app import app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/', headers={'x-api-key': '2c2bc4bc932e61c4365a4422a4bea47b'})
        self.assertEqual(response.status_code, 200)

    def test_chat(self):
        response = self.app.post('/chat', 
                                 json={'content': 'Hello!'},
                                 headers={'x-api-key': '2c2bc4bc932e61c4365a4422a4bea47b'})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
