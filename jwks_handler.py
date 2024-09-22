# jwks_handler.py
import time

def get_jwks(keys):
    return {
        "keys": [
            {
                "kty": "RSA",
                "n": key.get('public_key_n'),
                "e": key.get('public_key_e'),
                "kid": key.get('kid'),  # Safely get 'kid'
                "expiry": key.get('expiry')
            } for key in keys if key.get('expiry', 0) > time.time()
        ]
    }
