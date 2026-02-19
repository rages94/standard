from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from src.common.models.mixins import TimestampMixin
from src.domain.achievements.dto.enums import (
    AchievementCategory,
    ConditionType,
    MetaTier,
    RarityType,
    TimePeriod,
)

if TYPE_CHECKING:
    from src.data.models import Standard, UserAchievement, UserAchievementProgress


class Achievement(SQLModel, TimestampMixin, table=True):
    __tablename__ = "achievement"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    description: str
    icon: str | None = Field(default=None)
    category: AchievementCategory = Field(index=True)
    rarity: RarityType = Field(default=RarityType.COMMON)
    condition_type: ConditionType = Field(index=True)
    standard_id: UUID | None = Field(
        default=None, foreign_key="standard.id", nullable=True
    )
    target_value: float = Field(default=1000)
    time_period: TimePeriod | None = Field(default=None, nullable=True)
    parent_meta_achievement_id: UUID | None = Field(
        default=None, foreign_key="achievement.id", nullable=True
    )
    meta_tier: MetaTier | None = Field(default=None, nullable=True)
    is_meta_group: bool = Field(default=False)
    is_active: bool = Field(default=True)

    standard: "Standard" = Relationship()
    user_achievements: list["UserAchievement"] = Relationship(
        back_populates="achievement"
    )
    progress_records: list["UserAchievementProgress"] = Relationship(
        back_populates="achievement"
    )


class AchievementPublic(SQLModel):
    id: UUID
    name: str
    description: str
    icon: str | None
    category: AchievementCategory
    rarity: RarityType
    condition_type: ConditionType
    target_value: float
    time_period: TimePeriod | None
    meta_tier: MetaTier | None
    is_meta_group: bool
    is_active: bool


class AchievementCreate(SQLModel):
    name: str
    description: str
    icon: str | None = None
    category: AchievementCategory
    rarity: RarityType = RarityType.COMMON
    condition_type: ConditionType
    standard_id: UUID | None = None
    target_value: float = 100
    time_period: TimePeriod | None = None
    parent_meta_achievement_id: UUID | None = None
    meta_tier: MetaTier | None = None
    is_meta_group: bool = False
    is_active: bool = True


class AchievementUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    icon: str | None = None
    category: AchievementCategory | None = None
    rarity: RarityType | None = None
    condition_type: ConditionType | None = None
    standard_id: UUID | None = None
    target_value: float | None = None
    time_period: TimePeriod | None = None
    parent_meta_achievement_id: UUID | None = None
    meta_tier: MetaTier | None = None
    is_meta_group: bool | None = None
    is_active: bool | None = None
