"""Repository handling persistence of tasks."""

from contextlib import AbstractContextManager
from typing import Callable, Optional

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from datetime import datetime

from app.core.config import configs
from app.util.query_builder import dict_to_sqlalchemy_filter_options

from app.model.task import Task, TaskStatus
from app.repository.base_repository import BaseRepository


class TaskRepository(BaseRepository):
    """Provides task specific queries."""

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Task)

    def read_by_options(self, schema, eager: bool = False):
        schema_dict = schema.model_dump(exclude_none=True)
        search = schema_dict.pop("search", None)
        ordering = schema_dict.get("ordering", configs.ORDERING)
        order_query = (
            getattr(self.model, ordering[1:]).desc()
            if ordering.startswith("-")
            else getattr(self.model, ordering).asc()
        )
        page = schema_dict.get("page", configs.PAGE)
        page_size = schema_dict.get("page_size", configs.PAGE_SIZE)

        if isinstance(page, str) and page.isdigit():
            page = int(page)
        if isinstance(page_size, str) and page_size != "all" and page_size.isdigit():
            page_size = int(page_size)

        filter_options = dict_to_sqlalchemy_filter_options(self.model, schema_dict)
        if search:
            search_filter = or_(
                self.model.title.ilike(f"%{search}%"),
                self.model.description.ilike(f"%{search}%"),
            )
            filter_options = and_(filter_options, search_filter)

        with self.session_factory() as session:
            query = session.query(self.model)
            if eager:
                for eager in getattr(self.model, "eagers", []):
                    query = query.options(joinedload(getattr(self.model, eager)))
            filtered_query = query.filter(filter_options)
            query = filtered_query.order_by(order_query)
            if page_size == "all":
                query = query.all()
            else:
                query = query.limit(page_size).offset((page - 1) * page_size).all()
            total_count = filtered_query.count()
            return {
                "founds": query,
                "search_options": {
                    "page": page,
                    "page_size": page_size,
                    "ordering": ordering,
                    "total_count": total_count,
                },
            }

    def get_stats(self, user_id: Optional[str] = None):
        """Return aggregated task statistics."""
        with self.session_factory() as session:
            query = session.query(self.model)
            if user_id:
                query = query.filter(self.model.user_id == user_id)
            tasks = query.all()
            total = len(tasks)
            completed = len([t for t in tasks if t.status == TaskStatus.completed])
            pending = len([t for t in tasks if t.status == TaskStatus.pending])
            overdue = len(
                [
                    t
                    for t in tasks
                    if t.due_date
                    and datetime.fromisoformat(str(t.due_date)) < datetime.utcnow()
                    and t.status != TaskStatus.completed
                ]
            )
            return {
                "total": total,
                "completed": completed,
                "pending": pending,
                "overdue": overdue,
            }
