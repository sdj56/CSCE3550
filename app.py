from flask import Flask, request, jsonify, Response
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import base64
import jwt
import datetime
import time

app = Flask(__name__)

# Generate two RSA key pairs: one valid, one expired
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
expired_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Serialize private keys to PEM
pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)
expired_pem = expired_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

# Get RSA key numbers
numbers = private_key.private_numbers()


# Utility: Convert an integer to Base64 URL-safe encoding
def int_to_base64(value):
    value_hex = format(value, 'x')
    if len(value_hex) % 2 == 1:
        value_hex = '0' + value_hex
    value_bytes = bytes.fromhex(value_hex)
    encoded = base64.urlsafe_b64encode(value_bytes).rstrip(b'=')
    return encoded.decode('utf-8')


# JWT Generation Route
@app.route('/auth', methods=['POST'])
def auth():
    # Check if an expired token is requested
    expired = request.args.get('expired', 'false').lower() == 'true'
    
    # JWT headers and payload
    headers = {
        "kid": "goodKID"
    }
    token_payload = {
        "user": "username",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    
    # Handle expired token generation
    if expired:
        headers["kid"] = "expiredKID"
        token_payload["exp"] = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
        encoded_jwt = jwt.encode(token_payload, expired_pem, algorithm="RS256", headers=headers)
    else:
        encoded_jwt = jwt.encode(token_payload, pem, algorithm="RS256", headers=headers)
    
    # Return the JWT in both "jwt" and "token" fields
    return jsonify({"jwt": encoded_jwt, "token": encoded_jwt}), 200


# JWKS Route
@app.route('/.well-known/jwks.json', methods=['GET'])
def jwks():
    # Return the public key in JWKS format
    jwks_keys = {
        "keys": [
            {
                "alg": "RS256",
                "kty": "RSA",
                "use": "sig",
                "kid": "goodKID",
                "n": int_to_base64(numbers.public_numbers.n),
                "e": int_to_base64(numbers.public_numbers.e),
            }
        ]
    }
    return jsonify(jwks_keys), 200


# Return 405 for methods that aren't supported on certain endpoints
@app.route('/auth', methods=['GET', 'PUT', 'DELETE', 'PATCH', 'HEAD'])
@app.route('/.well-known/jwks.json', methods=['POST', 'PUT', 'DELETE', 'PATCH'])
def method_not_allowed():
    return Response(status=405)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
