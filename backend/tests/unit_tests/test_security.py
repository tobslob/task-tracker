from datetime import timedelta

import pytest

from app.core.security import create_access_token, decode_jwt, JWTBearer
from app.core.exceptions import AuthError


def test_decode_jwt_invalid_token():
    with pytest.raises(AuthError):
        decode_jwt("invalid.token")


def test_decode_jwt_expired_token():
    token, _ = create_access_token({"sub": "1"}, expires_delta=timedelta(seconds=-1))
    with pytest.raises(AuthError):
        decode_jwt(token)


def test_verify_jwt_invalid_token():
    bearer = JWTBearer()
    assert bearer.verify_jwt("invalid.token") is False


def test_verify_jwt_expired_token():
    token, _ = create_access_token({"sub": "1"}, expires_delta=timedelta(seconds=-1))
    bearer = JWTBearer()
    assert bearer.verify_jwt(token) is False
