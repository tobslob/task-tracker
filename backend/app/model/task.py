from enum import Enum
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship
from sqlalchemy import Column, ForeignKey, String

from app.model.base_model import BaseModel

if TYPE_CHECKING:
    from app.model.user import User


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in-progress"
    completed = "completed"


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Task(BaseModel, table=True):
    """Task model storing user tasks."""

    # reference the owning user without cascading deletion
    user_id: str = Field(
        sa_column=Column("user_id", String, ForeignKey("user.id", ondelete="RESTRICT"))
    )
    user: Optional["User"] = Relationship(back_populates="tasks")
    title: str = Field()
    description: Optional[str] = Field(default=None, nullable=True)
    status: TaskStatus = Field(default=TaskStatus.pending)
    priority: TaskPriority = Field(default=TaskPriority.medium)
    due_date: str = Field()
