from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel

from src.common.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from src.data.models import User


def get_expire_date(hours=1):
    return datetime.now(UTC) + timedelta(hours=hours)


class AuthLink(TimestampMixin, SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID | None = Field(foreign_key="user.id", nullable=True)
    expire_datetime: datetime = Field(
        default_factory=get_expire_date,
        sa_column=Column(DateTime(timezone=True), index=True),
    )

    user: "User" = Relationship(back_populates="auth_links")


class UserBotLogin(SQLModel):
    username: str
    password: str
    token: str
    chat_id: int
