import json
import os

from sqlmodel import SQLModel, Session, create_engine, select

from app.core.config import configs
from app.model.user import User
from app.model.task import Task
from app.core.security import get_password_hash


def main() -> None:
    engine = create_engine(configs.DATABASE_URI, echo=True)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        with open("seeds/users.json") as f:
            users = json.load(f)

        user_name_map: dict[str, str] = {}
        for user in users:
            user_obj = User(
                email=user["email"],
                password=get_password_hash(user["password"]),
                name=user.get("name"),
                is_active=user.get("is_active", True),
                is_superuser=user.get("is_superuser", False),
            )
            session.add(user_obj)
            if user.get("name"):
                user_name_map[user["name"]] = user_obj.id

        session.flush()

        with open("seeds/tasks.json") as f:
            tasks = json.load(f)
        for task in tasks:
            owner_name = task["user_id"]
            owner_id = user_name_map.get(owner_name)
            if owner_id is None:
                continue
            session.add(
                Task(
                    user_id=owner_id,
                    title=task.get("title"),
                    description=task.get("description"),
                    status=task.get("status", "pending"),
                    priority=task.get("priority", "medium"),
                    due_date=task["due_date"],
                )
            )

        session.commit()

        email = os.getenv("SUPERUSER_EMAIL")
        password = os.getenv("SUPERUSER_PASSWORD")
        name = os.getenv("SUPERUSER_NAME")
        if email and password:
            session.add(
                User(
                    email=email,
                    password=get_password_hash(password),
                    name=name,
                    is_active=True,
                    is_superuser=True,
                )
            )
            session.commit()

        email = os.getenv("SUPERUSER_EMAIL")
        password = os.getenv("SUPERUSER_PASSWORD")
        name = os.getenv("SUPERUSER_NAME")
        if email and password:
            existing = session.exec(
                select(User).where(User.email == email)).first()
            if not existing:
                session.add(
                    User(
                        email=email,
                        password=get_password_hash(password),
                        name=name,
                        is_active=True,
                        is_superuser=True,
                    )
                )
                session.commit()


if __name__ == "__main__":
    main()
