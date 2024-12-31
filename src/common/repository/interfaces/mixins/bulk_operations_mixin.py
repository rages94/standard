from typing import Protocol

from sqlalchemy.sql import Select


class BulkOperationsMixinI(Protocol):
    bulk_delete_query: Select | None = None

    async def bulk_create(self, data: list[dict]) -> None: ...

    async def bulk_insert(self, data: list[dict]) -> None: ...

    async def bulk_update(self, data: list[dict], by_field: str = "id") -> None: ...
    async def bulk_update_by_pk(self, data: list[dict]) -> None: ...

    async def bulk_delete(self, params: dict) -> None: ...

    async def bulk_upsert(
        self,
        data: list[dict],
        params: dict | None = None,
        exclude_from_update: list[str] | None = None,
    ) -> None: ...
