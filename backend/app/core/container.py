from app.core.config import configs
from app.core.database import Database
from app.repository.task_repository import TaskRepository
from app.repository.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.task_service import TaskService
from app.services.user_service import UserService
from dependency_injector import containers, providers

modules = [
    "app.api.v1.endpoints.auth",
    "app.api.v1.endpoints.user",
    "app.api.v1.endpoints.task",
    "app.core.dependencies",
]
if configs.ENV == "dev":
    modules.append("app.api.dev.endpoints.superuser")


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=modules)

    db = providers.Singleton(Database, db_url=configs.DATABASE_URI)

    task_repository = providers.Factory(TaskRepository, session_factory=db.provided.session)
    user_repository = providers.Factory(UserRepository, session_factory=db.provided.session)

    auth_service = providers.Factory(AuthService, user_repository=user_repository)
    task_service = providers.Factory(TaskService, task_repository=task_repository)
    user_service = providers.Factory(UserService, user_repository=user_repository)
