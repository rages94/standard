import telegramify_markdown
from telegram import Update
from telegram.constants import ParseMode

from src.data.models import User
from src.domain.bot.interfaces import IHandler
from src.domain.completed_standards.use_cases.create_from_text import CreateCompletedStandardsFromText
from src.domain.user.use_cases.get import GetUser


class CreateCompletedStandardHandler(IHandler):
    def __init__(
        self,
        create_completed_standards_from_text: CreateCompletedStandardsFromText,
        get_user: GetUser,
    ):
        self.create_completed_standards_from_text = create_completed_standards_from_text
        self.get_user = get_user

    async def __call__(self, update: Update, user: User) -> str:
        input_message = update.message.text
        created_standards = await self.create_completed_standards_from_text(
            input_message, user.id, user.completed_type
        )
        user = await self.get_user(user.id)

        if created_standards:
            result = (
                "Списываю:\n"
                + "\n".join(f"- {k}: {v}" for k, v in created_standards.items())
            )
            result += f"\n\n**Оставшийся долг**: {user.total_liabilities} н."
        else:
            result = "Нифига не понял, что списать?"

        await update.message.reply_text(
            telegramify_markdown.markdownify(result),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return result
