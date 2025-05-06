from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship

from src.data.models.standard import StandardPublic
from src.domain.user.dto.enums import CompletedType

if TYPE_CHECKING:
    from src.data.models import User, Standard


class CompletedStandard(SQLModel, table=True):
    __tablename__ = "completed_standard"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    standard_id: UUID = Field(foreign_key="standard.id")
    count: int
    user_id: UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)

    user: "User" = Relationship(back_populates="completed_standards")
    standard: "Standard" = Relationship(back_populates="completed_standards")


class CompletedStandardCreate(SQLModel):
    standard_id: UUID
    count: int
    completed_type: CompletedType

    def completed_type_is_count(self) -> bool:
        return self.completed_type == CompletedType.count


class CompletedStandardUpdate(SQLModel):
    standard_id: UUID | None = None
    count: int | None = None


class CompletedStandardPublic(SQLModel):
    id: UUID
    count: int
    created_at: datetime
    standard: StandardPublic
