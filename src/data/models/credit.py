from datetime import datetime, date
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from src.data.models import User


class Credit(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    count: int
    completed_count: int
    user_id: UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)
    deadline_date: date = Field(default_factory=datetime.now)

    user: "User" = Relationship(back_populates="credits")
