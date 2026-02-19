from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from passlib.context import CryptContext
from sqlmodel import Field, Relationship, SQLModel

from src.common.models.mixins import TimestampMixin
from src.domain.user.dto.enums import CompletedType

if TYPE_CHECKING:
    from src.data.models import (
        AuthLink,
        CompletedStandard,
        Credit,
        Liability,
        LiabilityTemplate,
        Message,
        UserAchievement,
        UserAchievementProgress,
        UserStreak,
    )

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(TimestampMixin, SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str | None = Field(unique=True, index=True)
    hashed_password: str
    weight: float = Field(
        default=70, nullable=False, sa_column_kwargs={"server_default": "70"}
    )
    sex: str = Field(
        default="male", nullable=False, sa_column_kwargs={"server_default": "male"}
    )
    birthday: datetime | None = Field(nullable=True)
    total_liabilities: float | None = Field(default=0, nullable=True)
    telegram_chat_id: int | None = Field(nullable=True, index=True)
    completed_type: str | None = Field(CompletedType.count.value, nullable=True)

    completed_standards: list["CompletedStandard"] = Relationship(back_populates="user")
    liabilities: list["Liability"] = Relationship(back_populates="user")
    messages: list["Message"] = Relationship(back_populates="user")
    credits: list["Credit"] = Relationship(back_populates="user")
    liability_templates: list["LiabilityTemplate"] = Relationship(back_populates="user")
    auth_links: list["AuthLink"] = Relationship(back_populates="user")
    achievements: list["UserAchievement"] = Relationship(back_populates="user")
    achievement_progress: list["UserAchievementProgress"] = Relationship(
        back_populates="user"
    )
    streak: "UserStreak" = Relationship(back_populates="user")

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    def check_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)


class UserPublic(SQLModel):
    id: UUID
    username: str
    email: str | None
    created_at: datetime
    weight: float
    sex: str
    birthday: datetime | None
    total_liabilities: float | None
    completed_type: str | None


class UserCreate(SQLModel):
    username: str
    password: str


class UserUpdate(SQLModel):
    email: str | None = None
    completed_type: CompletedType | None = None
    weight: float | None = None
    sex: str | None = None
    birthday: datetime | None = None


class UserLogin(SQLModel):
    username: str
    password: str
