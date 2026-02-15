from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel

from src.common.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from src.data.models import User


class Credit(SQLModel, TimestampMixin, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    count: float
    completed_count: float
    user_id: UUID = Field(foreign_key="user.id")
    deadline_date: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    completed_at: datetime | None = Field(sa_column=Column(DateTime(timezone=True)))
    completed: bool | None = Field(None)

    user: "User" = Relationship(back_populates="credits")


class CreditPublic(SQLModel):
    id: UUID
    count: float
    completed_count: float
    created_at: datetime
    deadline_date: datetime
    completed_at: datetime | None
    completed: bool | None
