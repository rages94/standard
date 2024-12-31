from typing import Protocol
from uuid import UUID

IdType = int | UUID | str


class DeleteMixinI(Protocol):
    async def delete(self, object_id: IdType) -> None: ...
