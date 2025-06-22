from sqlalchemy.exc import NoResultFound

from src.data.models import User
from src.data.uow import UnitOfWork
from src.domain.user.dto.filters import UserFilterSchema


class AuthChatManager:
    def __init__(self, uow: UnitOfWork):
        self.auth_chats: dict[int, User] = dict()
        self.uow = uow

    def add_auth_chat(self, chat_id: int, user: User) -> None:
        self.auth_chats[chat_id] = user

    def remove_auth_chat(self, chat_id: int) -> None:
        self.auth_chats.pop(chat_id, None)

    async def get_auth_user(self, chat_id: int) -> User | None:
        user = self.auth_chats.get(chat_id, None)
        if not user:
            async with self.uow:
                try:
                    user = await self.uow.user_repo.get_one(
                        UserFilterSchema(chat_id=chat_id).model_dump(exclude_unset=True)
                    )
                except NoResultFound:
                    return None
        self.add_auth_chat(chat_id, user)
        return user