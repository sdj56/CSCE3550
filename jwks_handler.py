from flask import jsonify
import time

def get_jwks(keys):
    # Only return keys that are not expired
    jwks_keys = [
        {
            "kty": "RSA",
            "use": "sig",
            "kid": key['kid'],
            "n": key['public_key'],  # The public key in your JWKS response
        }
        for key in keys if key['expiry'] > time.time()  # Only return unexpired keys
    ]
    
    return jsonify({"keys": jwks_keys})
