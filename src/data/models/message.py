from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import func
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from src.data.models import User


class Message(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    text: str
    user_id: UUID | None = Field(foreign_key="user.id", nullable=True)
    chat_id: int
    updated_at: datetime | None = Field(
        default=None,
        sa_column_kwargs={"onupdate": func.now(), "nullable": True},
    )
    created_at: datetime = Field(default_factory=datetime.now)

    user: "User" = Relationship(back_populates="messages")


class MessageCreate(SQLModel):
    text: str
    chat_id: int
    user_id: UUID | None = None


class MessageUpdate(SQLModel):
    text: str


class MessagePublic(SQLModel):
    id: UUID
    text: str
    chat_id: int
    updated_at: datetime | None = None
    created_at: datetime
    user_id: UUID | None = None
