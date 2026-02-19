from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from src.common.models.mixins import TimestampMixin
from src.data.models.standard import StandardPublic
from src.domain.user.dto.enums import CompletedType

if TYPE_CHECKING:
    from src.data.models import Standard, User


class CompletedStandard(SQLModel, TimestampMixin, table=True):
    __tablename__ = "completed_standard"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    standard_id: UUID = Field(foreign_key="standard.id")
    count: float
    weight: float | None
    user_weight: float | None
    total_norm: float | None
    user_id: UUID = Field(foreign_key="user.id")

    user: "User" = Relationship(back_populates="completed_standards")
    standard: "Standard" = Relationship(back_populates="completed_standards")


class CompletedStandardCreate(SQLModel):
    standard_id: UUID
    count: float
    weight: float | None = None
    user_weight: float | None = None
    total_norm: float | None = None
    completed_type: CompletedType

    def completed_type_is_count(self) -> bool:
        return self.completed_type == CompletedType.count


class CompletedStandardUpdate(SQLModel):
    standard_id: UUID | None = None
    count: float | None = None
    weight: float | None = None


class CompletedStandardPublic(SQLModel):
    id: UUID
    count: float
    weight: float | None = None
    user_weight: float | None = None
    total_norm: float | None = None
    created_at: datetime
    standard: StandardPublic | None = None
    user_id: UUID
