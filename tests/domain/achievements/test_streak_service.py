"""Тесты для сервиса достижений - тестирование логики стриков"""

from datetime import date, datetime, timedelta
from uuid import UUID

import pytest

from src.data.models import User, UserStreak
from src.domain.achievements.services.achievement_service import AchievementService


@pytest.fixture
async def achievement_service(_container):
    """Фикстура AchievementService"""
    uow = _container.repositories.uow()
    async with uow:
        return AchievementService(uow)


class TestUpdateUserStreak:
    """Тесты метода update_user_streak"""

    async def test_first_activity_starts_streak_at_one(
        self, _container, default_user: User
    ) -> None:
        """Первая тренировка устанавливает стрик = 1"""
        uow = _container.repositories.uow()
        async with uow:
            service = AchievementService(uow)
            activity_date = date(2026, 3, 4)

            streak = await service.update_user_streak(default_user.id, activity_date)
            await uow.commit()

        assert streak.current_streak == 1
        assert streak.longest_streak == 1
        assert streak.last_activity_date == activity_date

    async def test_next_day_increments_by_delta(
        self, _container, default_user: User
    ) -> None:
        """Тренировка на следующий день (delta=1) увеличивает стрик на 1"""
        uow = _container.repositories.uow()
        start_date = date(2026, 3, 4)
        next_date = start_date + timedelta(days=1)

        async with uow:
            service = AchievementService(uow)
            await service.update_user_streak(default_user.id, start_date)
            await uow.commit()
            streak = await service.update_user_streak(default_user.id, next_date)
            await uow.commit()

        assert streak.current_streak == 2
        assert streak.longest_streak == 2

    async def test_two_days_gap_increments_by_delta(
        self, _container, default_user: User
    ) -> None:
        """Тренировка через 2 дня (delta=2) увеличивает стрик на 2"""
        uow = _container.repositories.uow()
        start_date = date(2026, 3, 4)
        next_date = start_date + timedelta(days=2)

        async with uow:
            service = AchievementService(uow)
            await service.update_user_streak(default_user.id, start_date)
            await uow.commit()
            streak = await service.update_user_streak(default_user.id, next_date)
            await uow.commit()

        assert streak.current_streak == 3
        assert streak.longest_streak == 3

    async def test_three_days_gap_increments_by_delta(
        self, _container, default_user: User
    ) -> None:
        """Тренировка через 3 дня (delta=3) увеличивает стрик на 3"""
        uow = _container.repositories.uow()
        start_date = date(2026, 3, 4)
        next_date = start_date + timedelta(days=3)

        async with uow:
            service = AchievementService(uow)
            await service.update_user_streak(default_user.id, start_date)
            await uow.commit()
            streak = await service.update_user_streak(default_user.id, next_date)
            await uow.commit()

        assert streak.current_streak == 4
        assert streak.longest_streak == 4

    async def test_four_days_gap_resets_streak(
        self, _container, default_user: User
    ) -> None:
        """Тренировка через 4 дня (delta=4) сбрасывает стрик до 1"""
        uow = _container.repositories.uow()
        start_date = date(2026, 3, 4)
        next_date = start_date + timedelta(days=4)

        async with uow:
            service = AchievementService(uow)
            await service.update_user_streak(default_user.id, start_date)
            await uow.commit()
            streak = await service.update_user_streak(default_user.id, next_date)
            await uow.commit()

        assert streak.current_streak == 1

    async def test_same_day_no_change(self, _container, default_user: User) -> None:
        """Две тренировки в один день не меняют стрик"""
        uow = _container.repositories.uow()
        same_date = date(2026, 3, 4)

        async with uow:
            service = AchievementService(uow)
            await service.update_user_streak(default_user.id, same_date)
            await uow.commit()
            streak = await service.update_user_streak(default_user.id, same_date)
            await uow.commit()

        assert streak.current_streak == 1

    async def test_monday_to_thursday_streak_4(
        self, _container, default_user: User
    ) -> None:
        """Занимался в понедельник, потом в четверг - стрик = 4"""
        uow = _container.repositories.uow()
        monday = date(2026, 3, 2)
        thursday = monday + timedelta(days=3)

        async with uow:
            service = AchievementService(uow)
            await service.update_user_streak(default_user.id, monday)
            await uow.commit()
            streak = await service.update_user_streak(default_user.id, thursday)
            await uow.commit()

        assert streak.current_streak == 4


class TestCalculateStreakProgress:
    """Тесты метода calculate_streak_progress"""

    async def test_returns_current_streak_if_recent(
        self, _container, default_user: User
    ) -> None:
        """Возвращает текущий стрик если активность была <= 3 дней назад"""
        uow = _container.repositories.uow()
        today = datetime.now().date()

        async with uow:
            streak = UserStreak(
                user_id=default_user.id,
                current_streak=5,
                longest_streak=5,
                last_activity_date=today - timedelta(days=2),
            )
            uow.user_streak_repo.add(streak)
            await uow.commit()

            service = AchievementService(uow)
            result = await service.calculate_streak_progress(default_user.id)

        assert result == 5

    async def test_returns_zero_if_streak_broken(
        self, _container, default_user: User
    ) -> None:
        """Возвращает 0 если стрик прерван (>3 дней без активности)"""
        uow = _container.repositories.uow()

        async with uow:
            streak = UserStreak(
                user_id=default_user.id,
                current_streak=5,
                longest_streak=5,
                last_activity_date=date(2026, 3, 4) - timedelta(days=4),
            )
            uow.user_streak_repo.add(streak)
            await uow.commit()

            service = AchievementService(uow)
            result = await service.calculate_streak_progress(default_user.id)

        assert result == 0

    async def test_returns_zero_if_no_streak(
        self, _container, default_user: User
    ) -> None:
        """Возвращает 0 если стрик не создан"""
        uow = _container.repositories.uow()

        async with uow:
            service = AchievementService(uow)
            result = await service.calculate_streak_progress(default_user.id)

        assert result == 0
