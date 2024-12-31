from src.common.uow.uow import BaseUnitOfWork
from src.data.repositories.completed_standards import CompletedStandardRepository
from src.data.repositories.liabilities import LiabilityRepository
from src.data.repositories.liability_templates import LiabilityTemplateRepository
from src.data.repositories.standards import StandardRepository
from src.data.repositories.users import UserRepository


class UnitOfWork(BaseUnitOfWork):
    async def __aenter__(self) -> None:
        await super().__aenter__()
        self.user_repo = UserRepository(self.session)
        self.liability_repo = LiabilityRepository(self.session)
        self.liability_template_repo = LiabilityTemplateRepository(self.session)
        self.completed_standard_repo = CompletedStandardRepository(self.session)
        self.standard_repo = StandardRepository(self.session)
