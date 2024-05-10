# from typing import Dict
# from datetime import datetime, timedelta
# import jwt
# from decouple import config
# from app import setting


# JWT_SECRET = setting.SECRET_KEY
# JWT_ALGORITHM = setting.ALGORITHAM


# def token_response(token: str):
#     return {
#         "access_token": token
#     }


# def signJWT(user_id: str) -> Dict[str, str]:
#     expiration_datetime = datetime.utcnow() + timedelta(days=1)
#     expires = expiration_datetime.isoformat()
#     payload = {
#         "user_id": user_id,
#         "expires":  expires
#     }
#     token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

#     return token_response(token)


# def decodeJWT(token: str) -> dict:
#     try:
#         decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
#         return decoded_token if decoded_token["expires"] >= datetime.isoformat() else None
#     except:
#         return {}
    

# def get_current_user(token: str):
#     pyload = decodeJWT(token)
#     if pyload:
#         return pyload.get("sub")
    
#     else:
#         return None

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError
from decouple import config
from app import setting

secret_key = setting.SECRET_KEY
algoritham = setting.ALGORITHAM
accesstoken_expire_time = setting.ACCESSTOKEN_EXPIRE_TIME



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: int | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + timedelta(days=expires_delta)
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algoritham)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algoritham])
        # username: str = payload.get("first_name")
        if payload is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    

    return payload