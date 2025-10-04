from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, Relationship
from passlib.context import CryptContext

from src.domain.user.dto.enums import CompletedType

if TYPE_CHECKING:
    from src.data.models import AuthLink, CompletedStandard, Liability, LiabilityTemplate, Credit, Message

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str | None = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.now)
    total_liabilities: int | None = Field(default=0, nullable=True)
    telegram_chat_id: int | None = Field(nullable=True, index=True)
    completed_type: str = Field(CompletedType.count.value, nullable=True)

    completed_standards: list["CompletedStandard"] = Relationship(back_populates="user")
    liabilities: list["Liability"] = Relationship(back_populates="user")
    messages: list["Message"] = Relationship(back_populates="user")
    credits: list["Credit"] = Relationship(back_populates="user")
    liability_templates: list["LiabilityTemplate"] = Relationship(back_populates="user")
    auth_links: list["AuthLink"] = Relationship(back_populates="user")


    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    def check_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)



class UserCreate(SQLModel):
    username: str
    password: str


class UserUpdate(SQLModel):
    email: str | None = None
    completed_type: CompletedType | None = None


class UserLogin(SQLModel):
    username: str
    password: str
