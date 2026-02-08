from datetime import datetime, timezone

from sqlalchemy import func
from sqlmodel import Column, DateTime, Field


def utcnow():
    return datetime.now(timezone.utc)


class TimestampMixin:
    created_at: datetime = Field(
        default_factory=utcnow,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"server_default": func.now()},
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=utcnow,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"onupdate": utcnow, "server_default": func.now()},
        nullable=False,
    )
