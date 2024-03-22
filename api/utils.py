import hashlib
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import settings
from settings import SECRET_KEY


class Hasher:
    def get_password_hash(password: str) -> str:
        """
        Get hash of secret_key+password
        """
        return hashlib.sha256(f'{SECRET_KEY}{password}'.encode('utf8')).hexdigest()


def create_access_token(data: dict, expires_delta: Optional[timedelta]=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
