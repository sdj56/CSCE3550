from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import time
import uuid

def generate_key_pair():
    # Generate RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # Serialize keys to PEM format
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Generate a unique key ID and set an expiry timestamp
    kid = str(uuid.uuid4())
    expiry = int(time.time()) + 3600  # 1 hour from now

    return {
        "kid": kid,
        "private_key": private_pem.decode('utf-8'),  # Decode from bytes to string
        "public_key": public_pem.decode('utf-8'),    # Decode from bytes to string
        "expiry": expiry
    }
