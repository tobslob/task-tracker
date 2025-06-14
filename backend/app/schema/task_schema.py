from typing import List, Optional
from app.model.task import TaskPriority, TaskStatus

from pydantic import BaseModel, ConfigDict

from app.schema.base_schema import FindBase, ModelBaseInfo, SearchOptions
from app.util.schema import AllOptional


class BaseTask(BaseModel):
    user_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.pending
    priority: TaskPriority = TaskPriority.medium
    due_date: str

    model_config = ConfigDict(from_attributes=True)


class Task(ModelBaseInfo, BaseTask, metaclass=AllOptional):
    pass


class FindTask(FindBase, BaseTask, metaclass=AllOptional):
    """Schema for finding tasks with optional filters."""

    search: Optional[str] = None

    # allow exact matching by field when needed
    user_id__eq: str
    title__eq: str
    description__eq: str
    status__eq: TaskStatus
    priority__eq: TaskPriority


class TaskCreate(BaseTask):
    pass


class TaskUpdate(BaseTask, metaclass=AllOptional):
    pass


class FindTaskResult(BaseModel):
    founds: Optional[List[Task]]
    search_options: Optional[SearchOptions]


class TaskStats(BaseModel):
    """Summary statistics for tasks."""

    total: int
    completed: int
    pending: int
    overdue: int
