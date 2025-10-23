import telegramify_markdown
from telegram import Update
from telegram.constants import ParseMode

from src.domain.bot.interfaces import IHandler
from src.domain.liabilities.use_cases.create_from_text import CreateLiabilitiesFromText
from src.domain.user.use_cases.get import GetUser
from src.data.models import User


class CreateLiabilityHandler(IHandler):
    def __init__(
        self,
        create_liabilities_from_text: CreateLiabilitiesFromText,
        get_user: GetUser,
    ):
        self.create_liabilities_from_text = create_liabilities_from_text
        self.get_user = get_user

    async def __call__(self, update: Update, user: User) -> str:
        input_message = update.message.text
        created_liabilities = await self.create_liabilities_from_text(
            input_message, user.id
        )
        user = await self.get_user(user.id)

        if created_liabilities:
            result = "Записываю:\n" + "\n".join(
                f"- {k}: {v}" for k, v in created_liabilities.items()
            )
            result += f"\n\n**Текущий долг**: {user.total_liabilities} н."
        else:
            result = "Нифига не понял, что записать?"

        await update.message.reply_text(
            telegramify_markdown.markdownify(result),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return result
