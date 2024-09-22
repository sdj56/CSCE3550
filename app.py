# app.py
# The main application file that sets up the Flask web server and defines the endpoints.
# It uses the key manager, auth handler, and jwks handler modules.

from flask import Flask, request
from key_manager import generate_key_pair
from auth_handler import generate_jwt
from jwks_handler import get_jwks


from flask import Flask

app = Flask(__name__)

keys = []

# Route to generate keys (For testing/demo purposes)
@app.route('/generate_keys', methods=['POST'])
def generate_keys():
    key = generate_key_pair()
    keys.append(key)
    return {"status": "Key generated successfully"}, 201

# JWKS endpoint
@app.route('/jwks', methods=['GET'])
def jwks():
    return get_jwks(keys)

# Auth endpoint
@app.route('/auth', methods=['POST'])
def auth():
    expired = request.args.get('expired', 'false').lower() == 'true'
    return generate_jwt(keys, expired)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

@app.route('/')
def home():
    return 'Hello, world!', 200
