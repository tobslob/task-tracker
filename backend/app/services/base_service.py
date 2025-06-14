"""Shared base implementations for service objects."""

from typing import Any, Protocol


class RepositoryProtocol(Protocol):
    """Interface expected from repository classes."""

    def read_by_options(self, schema: Any) -> Any: ...

    def read_by_id(self, id: str) -> Any: ...

    def create(self, schema: Any) -> Any: ...

    def update(self, id: str, schema: Any) -> Any: ...

    def update_attr(self, id: str, attr: str, value: Any) -> Any: ...

    def whole_update(self, id: str, schema: Any) -> Any: ...

    def delete_by_id(self, id: str) -> Any: ...


class BaseService:
    """Provides basic CRUD operations using a repository."""

    def __init__(self, repository: RepositoryProtocol) -> None:
        self._repository = repository

    def get_list(self, schema: Any) -> Any:
        return self._repository.read_by_options(schema)

    def get_by_id(self, id: str) -> Any:
        return self._repository.read_by_id(id)

    def add(self, schema: Any) -> Any:
        return self._repository.create(schema)

    def patch(self, id: str, schema: Any) -> Any:
        return self._repository.update(id, schema)

    def patch_attr(self, id: str, attr: str, value: Any) -> Any:
        return self._repository.update_attr(id, attr, value)

    def put_update(self, id: str, schema: Any) -> Any:
        return self._repository.whole_update(id, schema)

    def remove_by_id(self, id: str) -> Any:
        return self._repository.delete_by_id(id)

    def close_scoped_session(self):
        self._repository.close_scoped_session()
