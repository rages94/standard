from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from src.data.models import User, Liability


class LiabilityTemplate(SQLModel, table=True):
    __tablename__ = "liability_template"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(unique=True)
    count: int
    user_id: UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)

    user: "User" = Relationship(back_populates="liability_templates")
    liabilities: list["Liability"] = Relationship(back_populates="liability_template")


class LiabilityTemplateCreate(SQLModel):
    name: str
    count: int


class LiabilityTemplateUpdate(SQLModel):
    name: str | None = None
    count: int | None = None


class LiabilityTemplatePublic(SQLModel):
    id: UUID
    name: str
