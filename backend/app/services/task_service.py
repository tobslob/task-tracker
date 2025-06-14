"""Service for task related operations."""

from typing import Optional

from app.repository.task_repository import TaskRepository
from app.services.base_service import BaseService
from app.model.task import TaskStatus


class TaskService(BaseService):
    """Manages tasks."""

    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
        super().__init__(task_repository)

    def mark_complete(self, task_id: str):
        """Mark a task as completed."""
        return self.patch_attr(task_id, "status", TaskStatus.completed)

    def get_stats(self, user_id: Optional[str] = None):
        """Return aggregated task statistics."""
        return self.task_repository.get_stats(user_id)
