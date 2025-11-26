from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship

from src.data.models.liability_template import LiabilityTemplatePublic

if TYPE_CHECKING:
    from src.data.models import User, LiabilityTemplate


class Liability(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    liability_template_id: UUID | None = Field(None, foreign_key="liability_template.id")
    count: float
    user_id: UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)

    user: "User" = Relationship(back_populates="liabilities")
    liability_template: "LiabilityTemplate" = Relationship(back_populates="liabilities")


class LiabilityCreate(SQLModel):
    liability_template_id: UUID | None = None
    count: float


class LiabilityUpdate(SQLModel):
    liability_template_id: UUID | None = None
    count: float | None = None


class LiabilityPublic(SQLModel):
    id: UUID
    count: float
    created_at: datetime
    liability_template: LiabilityTemplatePublic | None = None
