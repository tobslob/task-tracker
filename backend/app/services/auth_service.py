"""Authentication related service functions."""

from datetime import timedelta
from typing import List

from app.core.config import configs
from app.core.exceptions import AuthError
from app.core.security import create_access_token, get_password_hash, verify_password
from app.model.user import User
from app.repository.user_repository import UserRepository
from app.schema.auth_schema import Payload, SignIn, SignUp
from app.schema.user_schema import FindUser
from app.services.base_service import BaseService


class AuthService(BaseService):
    """Handles sign-in and sign-up actions."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    def sign_in(self, sign_in_info: SignIn):
        find_user = FindUser()
        find_user.email = sign_in_info.email
        user: List[User] = self.user_repository.read_by_options(find_user)["founds"]
        if len(user) < 1:
            raise AuthError(detail="Incorrect email or password")
        found_user = user[0]
        if not found_user.is_active:
            raise AuthError(detail="Account is not active")
        if not verify_password(sign_in_info.password, found_user.password):
            raise AuthError(detail="Incorrect email or password")
        delattr(found_user, "password")
        payload = Payload(
            id=found_user.id,
            email=found_user.email,
            name=found_user.name,
            is_superuser=found_user.is_superuser,
        )
        token_lifespan = timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token, expiration_datetime = create_access_token(payload.model_dump(), token_lifespan)
        sign_in_result = {
            "access_token": access_token,
            "expiration": expiration_datetime,
            "user_info": found_user,
        }
        return sign_in_result

    def sign_up(self, user_info: SignUp):
        user = User(
            **user_info.model_dump(exclude_none=True),
            is_active=True,
            is_superuser=False,
        )
        user.password = get_password_hash(user_info.password)
        created_user = self.user_repository.create(user)
        delattr(created_user, "password")
        return created_user

    def create_super_user(self, user_info: SignUp):
        """Create a superuser for development purposes."""
        user = User(
            **user_info.model_dump(exclude_none=True),
            is_active=True,
            is_superuser=True,
        )
        user.password = get_password_hash(user_info.password)
        created_user = self.user_repository.create(user)
        delattr(created_user, "password")
        return created_user

    def logout(self):
        """Placeholder logout to satisfy frontend."""
        return {"message": "Logged out"}
