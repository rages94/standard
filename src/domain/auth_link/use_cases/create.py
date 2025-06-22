from src.data.models import AuthLink
from src.data.uow import UnitOfWork


class CreateAuthLink:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def __call__(self, chat_id: int) -> AuthLink:
        async with self.uow:
            auth_link = AuthLink()
            self.uow.auth_link_repo.add(auth_link)
            await self.uow.commit()
            await self.uow.refresh(auth_link)
            return auth_link
