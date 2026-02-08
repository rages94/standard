from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, func
from sqlmodel import Boolean, Column, Field, Relationship, SQLModel

from src.common.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from src.data.models import CompletedStandard


class Standard(SQLModel, TimestampMixin, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(unique=True)
    normal_form: str | None = Field(nullable=True)
    count: Decimal | None = Field(nullable=True)
    is_deleted: bool = Field(
        sa_column=Column(Boolean, default=False, server_default="f", nullable=False)
    )

    completed_standards: list["CompletedStandard"] = Relationship(
        back_populates="standard"
    )


class StandardCreate(SQLModel):
    name: str
    count: Decimal | None = None


class StandardUpdate(SQLModel):
    name: str | None = None
    count: Decimal | None = None


class StandardPublic(SQLModel):
    id: UUID
    name: str
    normal_form: str | None = None
    count: Decimal | None = None
