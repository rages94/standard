from typing import Protocol


class CreateUpdateMixinI[SchemaOutType](Protocol):
    async def create(self, data: dict) -> SchemaOutType: ...

    async def update(self, data: dict) -> SchemaOutType: ...

    async def create_or_update(self, data: dict) -> SchemaOutType: ...
