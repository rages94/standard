from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy_filterset import (
    BaseFilterSet,
    Filter,
    InFilter,
    LimitOffsetFilter,
    OrderingField,
    OrderingFilter,
)

from src.common.repository.base import Repository
from src.data.models import (
    Achievement,
    UserAchievement,
    UserAchievementProgress,
    UserStreak,
)


class AchievementFilterSet(BaseFilterSet):
    id = Filter(Achievement.id)
    category = Filter(Achievement.category)
    condition_type = Filter(Achievement.condition_type)
    condition_types = InFilter(Achievement.condition_type)
    is_active = Filter(Achievement.is_active)
    rarity = Filter(Achievement.rarity)
    standard_id = Filter(Achievement.standard_id)
    parent_meta_achievement_id = Filter(Achievement.parent_meta_achievement_id)
    pagination = LimitOffsetFilter()
    order = OrderingFilter(
        created_at=OrderingField(Achievement.created_at),
    )


class AchievementRepository(
    Repository[Achievement, AchievementFilterSet, AsyncSession]
):
    model = Achievement
    filter_set = AchievementFilterSet


class UserAchievementFilterSet(BaseFilterSet):
    id = Filter(UserAchievement.id)
    user_id = Filter(UserAchievement.user_id)
    achievement_id = Filter(UserAchievement.achievement_id)
    pagination = LimitOffsetFilter()
    order = OrderingFilter(
        earned_at=OrderingField(UserAchievement.earned_at),
    )


class UserAchievementRepository(
    Repository[UserAchievement, UserAchievementFilterSet, AsyncSession]
):
    model = UserAchievement
    filter_set = UserAchievementFilterSet
    list_query = (
        select(UserAchievement)
        .options(joinedload(UserAchievement.achievement))
        .order_by(UserAchievement.earned_at.desc())
    )

    async def get_earned_achievement_ids(self, user_id: UUID) -> set[UUID]:
        query = select(UserAchievement.achievement_id).where(
            UserAchievement.user_id == user_id
        )
        result = await self.session.execute(query)
        return set(result.scalars().all())


class UserAchievementProgressFilterSet(BaseFilterSet):
    id = Filter(UserAchievementProgress.id)
    user_id = Filter(UserAchievementProgress.user_id)
    achievement_id = Filter(UserAchievementProgress.achievement_id)
    is_earned = Filter(UserAchievementProgress.is_earned)
    pagination = LimitOffsetFilter()


class UserAchievementProgressRepository(
    Repository[UserAchievementProgress, UserAchievementProgressFilterSet, AsyncSession]
):
    model = UserAchievementProgress
    filter_set = UserAchievementProgressFilterSet
    list_query = select(UserAchievementProgress).options(
        joinedload(UserAchievementProgress.achievement)
    )


class UserStreakFilterSet(BaseFilterSet):
    id = Filter(UserStreak.id)
    user_id = Filter(UserStreak.user_id)
    pagination = LimitOffsetFilter()


class UserStreakRepository(Repository[UserStreak, UserStreakFilterSet, AsyncSession]):
    model = UserStreak
    filter_set = UserStreakFilterSet
