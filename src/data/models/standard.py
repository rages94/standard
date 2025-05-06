from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship, Column, Boolean

if TYPE_CHECKING:
    from src.data.models import CompletedStandard


class Standard(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(unique=True)
    count: Decimal
    created_at: datetime = Field(default_factory=datetime.now)
    is_deleted: bool = Field(sa_column=Column(Boolean, default=False, server_default='f', nullable=False))

    completed_standards: list["CompletedStandard"] = Relationship(back_populates="standard")


class StandardCreate(SQLModel):
    name: str
    count: int


class StandardUpdate(SQLModel):
    name: str | None = None
    count: int | None = None


class StandardPublic(SQLModel):
    id: UUID
    name: str
