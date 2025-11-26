from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Boolean, Column, SQLModel, Field, Relationship

if TYPE_CHECKING:
    from src.data.models import User, Liability


class LiabilityTemplate(SQLModel, table=True):
    __tablename__ = "liability_template"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field()
    count: float
    normal_form: str | None = Field(nullable=True)
    is_deleted: bool = Field(sa_column=Column(Boolean, default=False, server_default='f', nullable=False))
    user_id: UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)

    user: "User" = Relationship(back_populates="liability_templates")
    liabilities: list["Liability"] = Relationship(back_populates="liability_template")


class LiabilityTemplateCreate(SQLModel):
    name: str
    count: float


class LiabilityTemplateUpdate(SQLModel):
    name: str | None = None
    count: float | None = None


class LiabilityTemplatePublic(SQLModel):
    id: UUID
    name: str
    count: float
    normal_form: str | None = None
