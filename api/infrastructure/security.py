import jwt
import datetime
import os

SECRET_KEY = os.getenv("JWT_SECRET", "supersecretkey")

def generate_token(payload, exp_minutes=5):
    """Genera un token JWT con expiración predeterminada."""
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(minutes=exp_minutes)
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token):
    """Decodifica un token JWT y valida su expiración."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
