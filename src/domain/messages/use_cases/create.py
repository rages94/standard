from src.data.models.message import MessageCreate, Message
from src.data.uow import UnitOfWork


class CreateMessage:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def __call__(self, body: MessageCreate):
        message = Message(text=body.text, user_id=body.user_id, chat_id=body.chat_id)
        async with self.uow:
            self.uow.liability_repo.add(message)

            await self.uow.commit()
            await self.uow.refresh(message)
        return message
