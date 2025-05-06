from pydantic import BaseModel

from src.data.models.liability import LiabilityPublic


class LiabilitiesListResponse(BaseModel):
    data: list[LiabilityPublic]
    count: int
    next_page: bool
