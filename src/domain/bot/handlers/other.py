from telegram import Update
from src.data.models import User
from src.domain.bot.interfaces import IHandler


class OtherHandler(IHandler):
    async def __call__(self, update: Update, user: User) -> str:
        result = "Хоп-хей"
        await update.message.reply_text(result)
        return result
