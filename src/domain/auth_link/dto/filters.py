from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AuthLinkFilterSchema(BaseModel):
    id: UUID | None = None
    user_id: UUID | None = None
    expire_datetime_gt: datetime | None = None
