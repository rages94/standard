from datetime import date

from pydantic import BaseModel

from src.data.models.completed_standard import CompletedStandardPublic

class Dataset(BaseModel):
    label: str
    data: list[int]


class GroupedCompletedStandard(BaseModel):
    labels: list[date]
    datasets: list[Dataset]


class UserCompletedStandard(BaseModel):
    username: str
    count: int


class RatingGroupedCompletedStandard(BaseModel):
    standard_name: str
    user_ratings: list[UserCompletedStandard]


class CompletedStandardListResponse(BaseModel):
    data: list[CompletedStandardPublic]
    count: int
    next_page: bool
