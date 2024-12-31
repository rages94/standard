from typing import Protocol


class RetrieveMixinI[SchemaOutType](Protocol):
    schema: SchemaOutType

    async def get_one(self, params: dict) -> SchemaOutType: ...
