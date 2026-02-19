from src.common.uow.uow import BaseUnitOfWork
from src.data.repositories.auth_link import AuthLinkRepository
from src.data.repositories.completed_standards import CompletedStandardRepository
from src.data.repositories.liabilities import LiabilityRepository
from src.data.repositories.liability_templates import LiabilityTemplateRepository
from src.data.repositories.message import MessageRepository
from src.data.repositories.standards import StandardRepository
from src.data.repositories.users import UserRepository
from src.data.repositories.credits import CreditRepository
from src.data.repositories.achievements import (
    AchievementRepository,
    UserAchievementProgressRepository,
    UserAchievementRepository,
    UserStreakRepository,
)


class UnitOfWork(BaseUnitOfWork):
    async def __aenter__(self) -> None:
        await super().__aenter__()
        self.user_repo = UserRepository(self.session)
        self.liability_repo = LiabilityRepository(self.session)
        self.liability_template_repo = LiabilityTemplateRepository(self.session)
        self.completed_standard_repo = CompletedStandardRepository(self.session)
        self.standard_repo = StandardRepository(self.session)
        self.credit_repo = CreditRepository(self.session)
        self.auth_link_repo = AuthLinkRepository(self.session)
        self.message_repo = MessageRepository(self.session)
        self.achievement_repo = AchievementRepository(self.session)
        self.user_achievement_repo = UserAchievementRepository(self.session)
        self.user_achievement_progress_repo = UserAchievementProgressRepository(
            self.session
        )
        self.user_streak_repo = UserStreakRepository(self.session)
