from datetime import datetime, timedelta
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from src.data.models import User


def get_expire_date(hours=1):
    return datetime.now() + timedelta(hours=hours)


class AuthLink(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)
    expire_datetime: datetime = Field(default_factory=get_expire_date, index=True)

    user: "User" = Relationship(back_populates="auth_links")


class UserBotLogin(SQLModel):
    username: str
    password: str
    token: str
    chat_id: int

