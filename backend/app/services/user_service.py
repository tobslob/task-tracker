"""Service for general user operations."""

from app.repository.user_repository import UserRepository
from app.services.base_service import BaseService


class UserService(BaseService):
    """Performs user CRUD operations."""
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)
