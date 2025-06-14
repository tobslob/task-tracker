from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends

from app.core.container import Container
from app.core.dependencies import get_current_active_user
from app.core.exceptions import AuthError
from app.core.middleware import inject
from app.model.user import User
from app.schema.base_schema import Blank
from app.schema.task_schema import (
    FindTask,
    FindTaskResult,
    TaskStats,
    Task,
    TaskCreate,
    TaskUpdate,
)
from app.services.task_service import TaskService

router = APIRouter(prefix="/task", tags=["task"])


@router.get("", response_model=FindTaskResult)
@inject
def get_task_list(
    find_query: FindTask = Depends(),
    service: TaskService = Depends(Provide[Container.task_service]),
    current_user: User = Depends(get_current_active_user),
):
    if not current_user.is_superuser:
        find_query.user_id__eq = current_user.id
    return service.get_list(find_query)


@router.get("/{task_id}", response_model=Task)
@inject
def get_task(
    task_id: str,
    service: TaskService = Depends(Provide[Container.task_service]),
    current_user: User = Depends(get_current_active_user),
):
    task = service.get_by_id(task_id)
    if not current_user.is_superuser and task.user_id != current_user.id:
        raise AuthError("Not authorized to access this task")
    return task


@router.post("", response_model=Task)
@inject
def create_task(
    task: TaskCreate,
    service: TaskService = Depends(Provide[Container.task_service]),
    current_user: User = Depends(get_current_active_user),
):
    task.user_id = current_user.id
    return service.add(task)


@router.patch("/{task_id}", response_model=Task)
@inject
def update_task(
    task_id: str,
    task: TaskUpdate,
    service: TaskService = Depends(Provide[Container.task_service]),
    current_user: User = Depends(get_current_active_user),
):
    return service.patch(task_id, task)


@router.post("/{task_id}/complete", response_model=Task)
@inject
def mark_complete_task(
    task_id: str,
    service: TaskService = Depends(Provide[Container.task_service]),
    current_user: User = Depends(get_current_active_user),
):
    """Mark a task as completed."""
    return service.mark_complete(task_id)


@router.get("/stats", response_model=TaskStats)
@inject
def get_task_stats(
    service: TaskService = Depends(Provide[Container.task_service]),
    current_user: User = Depends(get_current_active_user),
):
    """Return aggregated task statistics."""
    user_id = None if current_user.is_superuser else current_user.id
    return service.get_stats(user_id)


@router.delete("/{task_id}", response_model=Blank)
@inject
def delete_task(
    task_id: str,
    service: TaskService = Depends(Provide[Container.task_service]),
    current_user: User = Depends(get_current_active_user),
):
    service.remove_by_id(task_id)
    return Blank()
