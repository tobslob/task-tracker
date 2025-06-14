from datetime import datetime, timedelta, timezone
from typing import Tuple

from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
import logging
from passlib.context import CryptContext

from app.core.config import configs
from app.core.exceptions import AuthError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


def create_access_token(
    subject: dict, expires_delta: timedelta = None
) -> Tuple[str, str]:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    payload = {"exp": expire, **subject}
    encoded_jwt = jwt.encode(payload, configs.SECRET_KEY, algorithm=ALGORITHM)
    expiration_datetime = expire.strftime(configs.DATETIME_FORMAT)
    return encoded_jwt, expiration_datetime


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


logger = logging.getLogger(__name__)


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, configs.SECRET_KEY, algorithms=ALGORITHM)
        return (
            decoded_token
            if decoded_token["exp"] >= int(round(datetime.now(timezone.utc).timestamp()))
            else None
        )
    except JWTError as e:
        logger.error("JWT decode error: %s", e)
        raise AuthError(detail="Could not decode credentials") from e


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise AuthError(detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise AuthError(detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise AuthError(detail="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str) -> bool:
        try:
            payload = decode_jwt(jwt_token)
        except AuthError:
            return False
        return bool(payload)
