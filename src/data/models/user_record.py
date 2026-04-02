from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from src.common.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from src.data.models import User


class UserRecord(SQLModel, TimestampMixin, table=True):
    __tablename__ = "user_records"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    type: str = Field(max_length=20)
    count: float

    user: "User" = Relationship(back_populates="user_records")


class UserRecordPublic(SQLModel):
    id: UUID
    user_id: UUID
    type: str
    count: float
