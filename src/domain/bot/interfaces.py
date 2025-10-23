from telegram import Update

from src.data.models import User


class IHandler:
    async def __call__(self, update: Update, user: User) -> str:
        ...
