from uuid import UUID

from pydantic import BaseModel


class LiabilityFilterSchema(BaseModel):
    user_id: UUID | None = None
    pagination: tuple[int, int] | None = None
