# tests/test_key_manager.py
import unittest
from key_manager import generate_key_pair

class KeyManagerTestCase(unittest.TestCase):
    def test_generate_key_pair(self):
        private_key, public_key = generate_key_pair()
        self.assertIsNotNone(private_key)
        self.assertIsNotNone(public_key)

if __name__ == '__main__':
    unittest.main()
