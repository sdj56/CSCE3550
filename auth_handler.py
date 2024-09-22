  # This is from the PyJWT library
import jwt
import time
from flask import jsonify, Response

def generate_jwt(keys, expired=False):
    # Find the key to use (expired or not)
    if expired:
        print("Looking for an expired key...")
        key = next((k for k in keys if k['expiry'] < time.time()), None)
    else:
        print("Looking for a valid key...")
        key = next((k for k in keys if k['expiry'] > time.time()), None)

    if not key:
        print("No suitable key found.")
        return Response("No suitable key found", status=400)

    print(f"Selected Key: {key}")

    # Create a JWT with the key
    payload = {
        "sub": "mock_user",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600 if not expired else int(time.time()) - 3600  # 1 hour in the future or past
    }

    try:
        # Generate the JWT
        token = jwt.encode(payload, key['private_key'], algorithm='RS256', headers={"kid": key['kid']})

        # Decode the token if it's returned as bytes (needed for PyJWT < v2.x)
        if isinstance(token, bytes):
            token = token.decode('utf-8')

        return jsonify({"token": token})
    except Exception as e:
        print(f"Error generating JWT: {str(e)}")
        return Response(f"Error generating JWT: {str(e)}", status=500)
