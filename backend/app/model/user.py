from typing import List

from sqlmodel import Field, Relationship

from app.model.base_model import BaseModel
from app.model.task import Task


class User(BaseModel, table=True):
    email: str = Field(unique=True)
    password: str = Field()

    name: str = Field(default=None, nullable=True)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)

    # establish relationship to tasks without cascading deletes
    tasks: List[Task] = Relationship(back_populates="user")
