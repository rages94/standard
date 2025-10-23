import telegramify_markdown
from telegram import Update
from telegram.constants import ParseMode

from src.data.models import User
from src.domain.bot.interfaces import IHandler


class TotalLiabilitiesHandler(IHandler):
    async def __call__(self, update: Update, user: User) -> str:
        result = f"**Долг**: {user.total_liabilities} н."
        await update.message.reply_text(
            telegramify_markdown.markdownify(result),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return result
