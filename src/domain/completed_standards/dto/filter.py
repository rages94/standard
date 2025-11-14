from datetime import datetime, date
from uuid import UUID

from pydantic import BaseModel


class CompletedStandardFilterSchema(BaseModel):
    user_id: UUID | None = None
    created_at_gte: datetime | date | None = None
    pagination: tuple[int, int] | None = None
