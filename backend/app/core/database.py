from contextlib import AbstractContextManager, contextmanager
from typing import Any, Generator

from sqlalchemy import create_engine, orm
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import as_declarative, declared_attr
from sqlalchemy.orm import Session


@as_declarative()
class BaseModel:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Database:
    def __init__(self, db_url: str) -> None:
        if db_url.startswith("sqlite") and ":memory:" in db_url:
            self._engine = create_engine(
                db_url,
                echo=True,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
            )
        else:
            self._engine = create_engine(db_url, echo=True)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def create_database(self) -> None:
        BaseModel.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Generator[Any, Any, AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
