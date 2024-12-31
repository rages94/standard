from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from src.data.models import CompletedStandard


class Standard(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(unique=True)
    count: int
    created_at: datetime = Field(default_factory=datetime.now)

    completed_standards: list["CompletedStandard"] = Relationship(back_populates="standard")


class StandardCreate(SQLModel):
    name: str
    count: int

class StandardUpdate(SQLModel):
    name: str | None = None
    count: int | None = None
