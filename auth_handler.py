import jwt
import time
from flask import jsonify, Response

def generate_jwt(keys, expired=False):
    # Find the key to use (expired or not)
    if expired:
        key = next((k for k in keys if k['expiry'] < time.time()), None)
    else:
        key = next((k for k in keys if k['expiry'] > time.time()), None)

    if not key:
        return Response("No suitable key found", status=400)

    # Create a JWT with the key
    payload = {
        "sub": "mock_user",
        "iat": int(time.time()),
        "exp": int(time.time()) - 3600 if expired else int(time.time()) + 3600  # Expired JWT if expired=True
    }

    try:
        # Generate JWT with PyJWT library
        token = jwt.encode(payload, key['private_key'], algorithm='RS256', headers={"kid": key['kid']})

        # Ensure the token is returned in both "jwt" and "token" formats for GradeBot compatibility
        return jsonify({"jwt": token, "token": token})
    except Exception as e:
        return Response(f"Error generating JWT: {str(e)}", status=500)
