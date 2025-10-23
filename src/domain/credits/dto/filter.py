from uuid import UUID

from pydantic import BaseModel


class CreditFilterSchema(BaseModel):
    user_id: UUID | None = None
    completed: bool | None = None
    pagination: tuple[int, int] | None = None
