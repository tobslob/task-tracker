"""Repository managing user persistence."""

from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from app.model.user import User
from app.repository.base_repository import BaseRepository


class UserRepository(BaseRepository):
    """Handles queries related to users."""
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, User)
