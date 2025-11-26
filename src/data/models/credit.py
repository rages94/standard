from datetime import datetime, date
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from src.data.models import User


class Credit(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    count: float
    completed_count: float
    user_id: UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)
    deadline_date: date = Field(default_factory=datetime.now)
    completed_at: datetime | None = Field(None)
    completed: bool | None = Field(None)

    user: "User" = Relationship(back_populates="credits")


class CreditPublic(SQLModel):
    id: UUID
    count: float
    completed_count: float
    created_at: datetime
    deadline_date: date
    completed_at: datetime | None
    completed: bool | None
