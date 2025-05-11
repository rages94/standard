from pydantic import BaseModel

from src.data.models.credit import CreditPublic


class CreditListResponse(BaseModel):
    data: list[CreditPublic]
    count: int
    next_page: bool
