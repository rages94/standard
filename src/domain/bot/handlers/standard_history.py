import telegramify_markdown
from telegram import Update
from telegram.constants import ParseMode

from src.data.models import User
from src.data.models.completed_standard import CompletedStandardPublic
from src.domain.bot.interfaces import IHandler
from src.domain.completed_standards.use_cases.list_from_text import ListCompletedStandardsFromText


class StandardHistoryHandler(IHandler):
    def __init__(self, list_completed_standards_from_text: ListCompletedStandardsFromText):
        self.list_completed_standards_from_text = list_completed_standards_from_text

    async def __call__(self, update: Update, user: User) -> str:
        result = "`История списаний`:\n\n"
        input_message = update.message.text
        completed_standards: list[CompletedStandardPublic] = await self.list_completed_standards_from_text(
            input_message, user.id
        )

        for i, completed_standard in enumerate(completed_standards):
            result += f"{i + 1}) {completed_standard.standard.name}: {completed_standard.count}\n"

        await update.message.reply_text(
            telegramify_markdown.markdownify(result),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return result
