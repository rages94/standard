"""Сервис для работы с достижениями - единая точка входа для всей логики"""

from datetime import date, datetime
from uuid import UUID

from sqlalchemy import func, select

from src.data.models import (
    Achievement,
    UserAchievement,
    UserAchievementProgress,
    UserStreak,
)
from src.data.models.completed_standard import CompletedStandard
from src.data.uow import UnitOfWork
from src.domain.achievements.dto.enums import (
    ConditionType,
    MetaTier,
    TimePeriod,
)
from src.domain.achievements.dto.schemas import (
    AchievementProgressSchema,
    EarnedAchievementSchema,
    UserStreakSchema,
)


class AchievementService:
    """Единый сервис для работы с достижениями

    Объединяет логику калькуляции прогресса, проверки условий и выдачи достижений.
    Работает через Unit of Work для атомарности операций.
    """

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    # ========== Калькуляция прогресса ==========

    async def calculate_count_progress(
        self,
        user_id: UUID,
        standard_id: UUID,
        time_period: TimePeriod | None,
    ) -> float:
        """Рассчитать прогресс по количеству повторений"""
        query = select(
            func.sum(CompletedStandard.count)
        ).where(  # TODO move to repository!!!
            CompletedStandard.user_id == user_id,
            CompletedStandard.standard_id == standard_id,
        )

        if time_period == TimePeriod.DAILY:
            today = datetime.now().date()
            query = query.where(func.date(CompletedStandard.created_at) == today)
        elif time_period == TimePeriod.MONTHLY:
            today = datetime.now().date()
            first_day = today.replace(day=1)
            query = query.where(func.date(CompletedStandard.created_at) >= first_day)

        result = await self.uow.user_achievement_progress_repo.session.execute(query)
        total = result.scalar()
        return float(total) if total else 0.0

    async def calculate_weight_progress(
        self,
        user_id: UUID,
        standard_id: UUID,
        time_period: TimePeriod | None,
    ) -> float:
        """Рассчитать прогресс по суммарному весу (count * weight)"""
        query = select(
            func.sum(CompletedStandard.count * CompletedStandard.weight)
        ).where(
            CompletedStandard.user_id == user_id,
            CompletedStandard.standard_id == standard_id,
            CompletedStandard.weight.isnot(None),
        )

        if time_period == TimePeriod.DAILY:
            today = datetime.now().date()
            query = query.where(func.date(CompletedStandard.created_at) == today)
        elif time_period == TimePeriod.MONTHLY:
            today = datetime.now().date()
            first_day = today.replace(day=1)
            query = query.where(func.date(CompletedStandard.created_at) >= first_day)

        result = await self.uow.user_achievement_progress_repo.session.execute(query)
        total = result.scalar()
        return float(total) if total else 0.0

    async def calculate_streak_progress(self, user_id: UUID) -> int:
        """Получить текущую серию дней"""
        streak = await self.uow.user_streak_repo.get_or_none({"user_id": user_id})

        if streak is None:
            return 0

        # Проверяем, что серия актуальна
        if streak.last_activity_date:
            today = datetime.now().date()
            delta = (today - streak.last_activity_date).days
            if delta > 1:
                # Серия прервалась
                return 0

        return streak.current_streak

    async def calculate_progress_for_achievement(
        self,
        user_id: UUID,
        achievement: Achievement,
    ) -> float:
        """Рассчитать прогресс для конкретного достижения"""
        if achievement.condition_type == ConditionType.COUNT:
            if achievement.standard_id is None:
                return 0.0
            return await self.calculate_count_progress(
                user_id, achievement.standard_id, achievement.time_period
            )

        elif achievement.condition_type == ConditionType.WEIGHT:
            if achievement.standard_id is None:
                return 0.0
            return await self.calculate_weight_progress(
                user_id, achievement.standard_id, achievement.time_period
            )

        elif achievement.condition_type == ConditionType.STREAK:
            return float(await self.calculate_streak_progress(user_id))

        elif achievement.condition_type == ConditionType.META:
            # Для мета-ачивок прогресс будет рассчитываться отдельно
            return 0.0

        return 0.0

    # ========== Управление прогрессом ==========

    async def has_achievement(self, user_id: UUID, achievement_id: UUID) -> bool:
        """Проверить, получил ли пользователь достижение"""
        record = await self.uow.user_achievement_repo.get_or_none(
            {"user_id": user_id, "achievement_id": achievement_id}
        )
        return record is not None

    async def update_user_progress(
        self,
        user_id: UUID,
        achievement_id: UUID,
        current_value: float,
        is_earned: bool = False,
    ) -> UserAchievementProgress:
        """Обновить или создать прогресс достижения"""
        progress = await self.uow.user_achievement_progress_repo.get_or_none(
            {"user_id": user_id, "achievement_id": achievement_id}
        )

        if progress:
            progress.current_value = current_value
            progress.is_earned = is_earned
            progress.updated_at = func.now()
            self.uow.user_achievement_progress_repo.add(progress)
        else:
            progress = UserAchievementProgress(
                user_id=user_id,
                achievement_id=achievement_id,
                current_value=current_value,
                is_earned=is_earned,
            )
            self.uow.user_achievement_progress_repo.add(progress)

        return progress

    async def grant_achievement_to_user(
        self,
        user_id: UUID,
        achievement_id: UUID,
        progress_value: float,
    ) -> UserAchievement:
        """Выдать достижение пользователю"""
        user_achievement = UserAchievement(
            user_id=user_id,
            achievement_id=achievement_id,
            progress_at_earned=progress_value,
        )
        self.uow.user_achievement_repo.add(user_achievement)
        return user_achievement

    async def revoke_achievement(
        self,
        user_id: UUID,
        achievement_id: UUID,
    ) -> bool:
        """Отозвать достижение у пользователя"""
        deleted = await self.uow.user_achievement_repo.delete_by_user_and_achievement(
            user_id, achievement_id
        )
        if deleted:
            progress = await self.uow.user_achievement_progress_repo.get_or_none(
                {"user_id": user_id, "achievement_id": achievement_id}
            )
            if progress:
                progress.is_earned = False
                self.uow.user_achievement_progress_repo.add(progress)
        return deleted

    # ========== Управление серией дней ==========

    async def get_or_create_user_streak(self, user_id: UUID) -> UserStreak:
        """Получить существующую серию или создать новую"""
        streak = await self.uow.user_streak_repo.get_or_none({"user_id": user_id})
        if streak:
            return streak

        streak = UserStreak(user_id=user_id)
        self.uow.user_streak_repo.add(streak)
        return streak

    async def update_user_streak(
        self,
        user_id: UUID,
        activity_date: date,
    ) -> UserStreak:
        """Обновить серию дней пользователя"""
        streak = await self.get_or_create_user_streak(user_id)

        if streak.last_activity_date is None:
            # Первая активность
            streak.current_streak = 1
            streak.longest_streak = 1
            streak.last_activity_date = activity_date
        else:
            delta = (activity_date - streak.last_activity_date).days

            if delta == 0:
                # Уже учтена сегодняшняя активность
                pass
            elif delta == 1:
                # Продолжаем серию
                streak.current_streak += 1
                streak.last_activity_date = activity_date
                if streak.current_streak > streak.longest_streak:
                    streak.longest_streak = streak.current_streak
            else:
                # Серия прервалась
                streak.current_streak = 1
                streak.last_activity_date = activity_date

        return streak

    # ========== Проверка и выдача достижений ==========

    async def check_and_update_single_achievement(
        self,
        user_id: UUID,
        achievement: Achievement,
    ) -> tuple[bool, bool]:
        """Проверить, выдать или отозвать достижение

        Returns:
            tuple[bool, bool]: (granted, revoked)
        """
        has_achievement = await self.has_achievement(user_id, achievement.id)

        current_value = await self.calculate_progress_for_achievement(
            user_id, achievement
        )
        meets_condition = current_value >= achievement.target_value

        is_earned = meets_condition

        await self.update_user_progress(
            user_id=user_id,
            achievement_id=achievement.id,
            current_value=current_value,
            is_earned=is_earned,
        )

        # STREAK ачивки не отзываются
        if achievement.condition_type == ConditionType.STREAK:
            if meets_condition and not has_achievement:
                await self.grant_achievement_to_user(
                    user_id=user_id,
                    achievement_id=achievement.id,
                    progress_value=current_value,
                )
                return (True, False)
            return (False, False)

        # COUNT/WEIGHT ачивки - полная логика
        if meets_condition and not has_achievement:
            await self.grant_achievement_to_user(
                user_id=user_id,
                achievement_id=achievement.id,
                progress_value=current_value,
            )
            return (True, False)
        elif not meets_condition and has_achievement:
            await self.revoke_achievement(user_id, achievement.id)
            return (False, True)

        return (False, False)

    async def check_meta_achievements(
        self, user_id: UUID
    ) -> tuple[list[Achievement], list[Achievement]]:
        """Проверить мета-достижения - выдать или отозвать

        Returns:
            tuple[list[Achievement], list[Achievement]]: (granted, revoked)
        """
        granted: list[Achievement] = []
        revoked: list[Achievement] = []

        earned_ids = await self.uow.user_achievement_repo.get_earned_achievement_ids(
            user_id
        )

        meta_achievements = await self.uow.achievement_repo.filter(
            {"condition_type": ConditionType.META}
        )

        for meta in meta_achievements:
            has_meta = meta.id in earned_ids
            meets_condition = await self._check_meta_condition(meta, earned_ids)

            if meets_condition and not has_meta:
                await self.grant_achievement_to_user(
                    user_id=user_id,
                    achievement_id=meta.id,
                    progress_value=float(len(earned_ids)),
                )
                granted.append(meta)
                earned_ids.add(meta.id)
            elif not meets_condition and has_meta:
                await self.revoke_achievement(user_id, meta.id)
                revoked.append(meta)
                earned_ids.discard(meta.id)

        return (granted, revoked)

    async def _check_meta_condition(
        self,
        meta_achievement: Achievement,
        earned_ids: set[UUID],
    ) -> bool:
        """Проверить условие мета-ачивки"""
        # Получаем все активные ачивки (кроме мета)
        all_achievements = await self.uow.achievement_repo.filter(
            {
                "is_active": True,
                "condition_types": [ConditionType.COUNT, ConditionType.WEIGHT],
            }
        )
        count_weight_achievements = [
            a
            for a in all_achievements
            if a.condition_type in [ConditionType.COUNT, ConditionType.WEIGHT]
            and a.is_active
        ]

        # Проверяем групповые ачивки (Эксперты) по флагу is_meta_group
        if meta_achievement.is_meta_group:
            return await self._check_group_meta(
                meta_achievement, earned_ids, all_achievements
            )

        # Проверяем по meta_tier (Начинающий/Спортсмен/Мастер/Легенда)
        if meta_achievement.meta_tier:
            return await self._check_tier_meta(
                meta_achievement, earned_ids, count_weight_achievements
            )

        return False

    async def _check_group_meta(
        self,
        meta_achievement: Achievement,
        earned_ids: set[UUID],
        all_achievements: list[Achievement],
    ) -> bool:
        """Проверить групповую мета-ачивку (Эксперт отжиманий и т.д.)"""
        # Находим все ачивки, относящиеся к этой группе
        # (те, у которых parent_meta_achievement_id указывает на текущую мета-ачивку)  # TODO set parent_meta_achievement_id
        required_achievements = [
            a
            for a in all_achievements
            if a.parent_meta_achievement_id == meta_achievement.id
            and a.id != meta_achievement.id
            and a.is_active
        ]

        if not required_achievements:
            return False

        required_ids = {a.id for a in required_achievements}
        return required_ids.issubset(earned_ids)

    async def _check_tier_meta(
        self,
        meta_achievement: Achievement,
        earned_ids: set[UUID],
        count_weight_achievements: list[Achievement],
    ) -> bool:
        """Проверить мета-ачивку по tier (Начинающий/Спортсмен/Мастер/Легенда)"""
        tier = meta_achievement.meta_tier

        if tier == MetaTier.LEGEND:
            # Легенда: все count/weight ачивки
            required_achievements = count_weight_achievements
        elif tier == MetaTier.MASTER:
            # Мастер спорта: все ачивки с target_value >= 10000
            required_achievements = [
                a for a in count_weight_achievements if a.target_value >= 10000
            ]
        elif tier == MetaTier.ATHLETE:
            # Спортсмен: все ачивки с target_value >= 1000
            required_achievements = [
                a for a in count_weight_achievements if a.target_value >= 1000
            ]
        elif tier == MetaTier.BEGINNER:
            # Начинающий: все ачивки с target_value >= 100
            required_achievements = [
                a for a in count_weight_achievements if a.target_value >= 100
            ]
        else:
            return False

        if not required_achievements:
            return False

        required_ids = {a.id for a in required_achievements}
        return required_ids.issubset(earned_ids)

    async def check_and_update_achievements(
        self,
        user_id: UUID,
        standard_id: UUID | None = None,
        activity_date: date | None = None,
    ) -> tuple[list[Achievement], list[Achievement]]:
        """Проверить, выдать или отозвать все достижения пользователя

        Returns:
            tuple[list[Achievement], list[Achievement]]: (granted, revoked)
        """
        granted: list[Achievement] = []
        revoked: list[Achievement] = []

        # 1. Обновляем серию дней
        if activity_date:
            await self.update_user_streak(user_id, activity_date)

        # 2. Проверяем ачивки типа COUNT и WEIGHT
        if standard_id:
            achievements = await self.uow.achievement_repo.filter(
                {
                    "condition_types": [ConditionType.COUNT, ConditionType.WEIGHT],
                    "is_active": True,
                }
            )
            for achievement in achievements:
                if achievement.standard_id and achievement.standard_id != standard_id:
                    continue
                g, r = await self.check_and_update_single_achievement(
                    user_id, achievement
                )
                if g:
                    granted.append(achievement)
                if r:
                    revoked.append(achievement)

        # 3. Проверяем ачивки типа STREAK
        streak_achievements = await self.uow.achievement_repo.filter(
            {"condition_type": ConditionType.STREAK}
        )
        for achievement in streak_achievements:
            g, r = await self.check_and_update_single_achievement(user_id, achievement)
            if g:
                granted.append(achievement)
            if r:
                revoked.append(achievement)

        # 4. Проверяем мета-ачивки
        meta_granted, meta_revoked = await self.check_meta_achievements(user_id)
        granted.extend(meta_granted)
        revoked.extend(meta_revoked)

        return (granted, revoked)

    # ========== Получение данных ==========

    async def get_user_progress_with_achievements(
        self,
        user_id: UUID,
    ) -> list[AchievementProgressSchema]:
        achievements = await self.uow.achievement_repo.filter({})
        return await self._build_achievement_progress(user_id, achievements)

    async def get_user_progress_with_achievements_by_standard(
        self,
        user_id: UUID,
        standard_id: UUID,
    ) -> list[AchievementProgressSchema]:
        achievements = await self.uow.achievement_repo.filter(
            {"standard_id": standard_id}
        )
        return await self._build_achievement_progress(user_id, achievements)

    async def _build_achievement_progress(
        self,
        user_id: UUID,
        achievements: list[Achievement],
    ) -> list[AchievementProgressSchema]:
        progress_records = await self.uow.user_achievement_progress_repo.filter(
            {"user_id": user_id}
        )
        progress_map = {p.achievement_id: p for p in progress_records}

        earned_records = await self.uow.user_achievement_repo.filter(
            {"user_id": user_id}
        )
        earned_map = {e.achievement_id: e for e in earned_records}

        result = []
        for achievement in achievements:
            progress = progress_map.get(achievement.id)
            earned = earned_map.get(achievement.id)

            current_value = progress.current_value if progress else 0.0

            result.append(
                AchievementProgressSchema(
                    id=achievement.id,
                    name=achievement.name,
                    description=achievement.description,
                    icon=achievement.icon,
                    rarity=achievement.rarity,
                    condition_type=achievement.condition_type,
                    target_value=achievement.target_value,
                    time_period=achievement.time_period,
                    is_active=achievement.is_active,
                    current_value=current_value,
                    percentage=min(
                        100.0, (current_value / achievement.target_value * 100)
                    )
                    if achievement.target_value > 0
                    else 0.0,
                    is_earned=earned is not None,
                    earned_at=earned.earned_at if earned else None,
                )
            )

        return result

    async def get_user_earned_achievements(
        self,
        user_id: UUID,
    ) -> list[EarnedAchievementSchema]:
        """Получить полученные достижения пользователя"""
        earned = await self.uow.user_achievement_repo.filter({"user_id": user_id})

        result = []
        for record in earned:
            result.append(
                EarnedAchievementSchema(
                    id=record.achievement.id,
                    name=record.achievement.name,
                    description=record.achievement.description,
                    icon=record.achievement.icon,
                    rarity=record.achievement.rarity,
                    earned_at=record.earned_at,
                    progress_at_earned=record.progress_at_earned,
                )
            )

        return result

    async def get_user_streak(self, user_id: UUID) -> UserStreakSchema | None:
        """Получить текущую серию дней пользователя"""
        streak = await self.uow.user_streak_repo.get_or_none({"user_id": user_id})

        if streak is None:
            return None

        return UserStreakSchema(
            current_streak=streak.current_streak,
            longest_streak=streak.longest_streak,
            last_activity_date=streak.last_activity_date,
        )
