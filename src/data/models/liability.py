from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from src.common.models.mixins import TimestampMixin
from src.data.models.liability_template import LiabilityTemplatePublic

if TYPE_CHECKING:
    from src.data.models import LiabilityTemplate, User


class Liability(SQLModel, TimestampMixin, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    liability_template_id: UUID | None = Field(
        None, foreign_key="liability_template.id"
    )
    count: float
    user_id: UUID = Field(foreign_key="user.id")

    user: "User" = Relationship(back_populates="liabilities")
    liability_template: "LiabilityTemplate" = Relationship(back_populates="liabilities")


class LiabilityCreate(SQLModel):
    liability_template_id: UUID | None = None
    count: float = Field(..., gt=0)


class LiabilityUpdate(SQLModel):
    liability_template_id: UUID | None = None
    count: float | None = Field(None, gt=0, description="Количество для обязательства")


class LiabilityPublic(SQLModel):
    id: UUID
    count: float
    created_at: datetime
    liability_template: LiabilityTemplatePublic | None = None
