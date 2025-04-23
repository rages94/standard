from datetime import date

from pydantic import BaseModel


class Dataset(BaseModel):
    label: str
    data: list[int]


class GroupedCompletedStandard(BaseModel):
    labels: list[date]
    datasets: list[Dataset]
