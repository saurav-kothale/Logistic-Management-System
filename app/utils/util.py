from typing import Dict
from datetime import datetime, timedelta
import jwt
from decouple import config


JWT_SECRET = config("SECRET_KEY")
JWT_ALGORITHM = config("ALGORITHAM")


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: str) -> Dict[str, str]:
    expiration_datetime = datetime.utcnow() + timedelta(days=1)
    expires = expiration_datetime.isoformat()
    payload = {
        "user_id": user_id,
        "expires":  expires
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= datetime.isoformat() else None
    except:
        return {}
    

def get_current_user(token: str):
    pyload = decodeJWT(token)
    return pyload.get("sub")