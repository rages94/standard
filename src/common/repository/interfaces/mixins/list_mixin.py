from typing import Protocol


class ListMixinI[ListSchemaOutType](Protocol):
    list_schema: ListSchemaOutType

    async def filter(self, params: dict) -> list[ListSchemaOutType]: ...

    async def count(self, params: dict) -> int: ...
