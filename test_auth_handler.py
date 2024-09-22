import unittest
from app import app  # Import the Flask app

class TestAuthHandler(unittest.TestCase):

    def setUp(self):
        # Setup the app and the test client
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        # Generate keys before testing the /auth endpoint
        response = self.client.post('/generate_keys')
        self.assertEqual(response.status_code, 201)  # Ensure the key generation is successful

    def test_generate_jwt_expired_key(self):
        print("Testing expired key...")
        response = self.client.post('/auth', data={'expired': 'true'})
        print(response.data)  # Print response content to debug
        self.assertEqual(response.status_code, 200)  # Ensure the request is successful

    def test_generate_jwt_valid_key(self):
        print("Testing valid key...")
        response = self.client.post('/auth', data={'expired': 'false'})
        print(response.data)  # Print response content to debug
        self.assertEqual(response.status_code, 200)  # Ensure the request is successful

if __name__ == '__main__':
    unittest.main()
