import unittest
from app import app  # Import the Flask app
from jwks_handler import get_jwks  # Ensure this is correctly imported

class TestJWKSHandler(unittest.TestCase):

    def setUp(self):
        # Set up the Flask test app and test client
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_get_jwks(self):
        # Simulate a GET request to the JWKS endpoint
        response = self.client.get('/jwks')
        self.assertEqual(response.status_code, 200)

        # Parse the response JSON
        jwks = response.get_json()
        self.assertIn('keys', jwks)  # Ensure 'keys' exists in the response

if __name__ == '__main__':
    unittest.main()
