import json
import os
from uuid import UUID, uuid5, NAMESPACE_DNS

import pytest

# Import the application package early so that compatibility patches in
# ``app.__init__`` take effect before third party libraries are loaded.
import app

os.environ["ENV"] = "test"
os.environ["DB"] = "sqlite"
os.environ["DB_MEMORY"] = "1"

if os.getenv("ENV") not in ["test"]:
    msg = f"ENV is not test, it is {os.getenv('ENV')}"
    pytest.exit(msg)

from fastapi.testclient import TestClient
from loguru import logger
from sqlmodel import SQLModel, create_engine
from sqlalchemy.pool import StaticPool

from app.core.config import configs
from app.core.container import Container
from app.main import AppCreator
from app.model.task import Task
from app.model.user import User
from app.core.security import get_password_hash


def _uid(name: str) -> str:
    """Return a deterministic UUID for a given name."""
    return str(uuid5(NAMESPACE_DNS, name))


def insert_default_data(conn):
    user_default_file = open("./tests/test_data/users.json", "r")
    user_default_data = json.load(user_default_file)

    user_ids = {}
    for user in user_default_data:
        user_id = _uid(user["name"])
        user_ids[user["name"]] = user_id
        conn.execute(
            User.__table__.insert(),
            {
                "id": user_id,
                "email": user["email"],
                "password": get_password_hash(user["password"]),
                "name": user["name"],
                "is_active": user["is_active"],
                "is_superuser": user["is_superuser"],
            },
        )

    task_default_file = open("./tests/test_data/tasks.json", "r")
    task_default_data = json.load(task_default_file)
    for task in task_default_data:
        conn.execute(
            Task.__table__.insert(),
            {
                "title": task["title"],
                "description": task.get("description"),
                "user_id": user_ids[task["user_id"]],
                "status": task.get("status", "pending"),
                "priority": task.get("priority", "medium"),
                "due_date": task["due_date"],
            },
        )


def reset_db(engine=None):
    if engine is None:
        if (
            configs.DATABASE_URI.startswith("sqlite")
            and ":memory:" in configs.DATABASE_URI
        ):
            engine = create_engine(
                configs.DATABASE_URI,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
            )
        else:
            engine = create_engine(configs.DATABASE_URI)
    logger.info(engine)
    with engine.begin() as conn:
        if configs.ENV == "test":
            SQLModel.metadata.drop_all(conn)
            SQLModel.metadata.create_all(conn)
            insert_default_data(conn)
        else:
            raise Exception("Not in test environment")
    return engine


@pytest.fixture
def client():
    app_creator = AppCreator()
    app = app_creator.app
    reset_db(app_creator.db._engine)
    with TestClient(app) as client:
        yield client


@pytest.fixture
def container():
    container = Container()
    reset_db(container.db()._engine)
    return container


@pytest.fixture
def test_name(request):
    return request.node.name
