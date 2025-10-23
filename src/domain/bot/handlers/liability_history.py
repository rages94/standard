import telegramify_markdown
from telegram import Update
from telegram.constants import ParseMode

from src.data.models import User
from src.data.models.liability import LiabilityPublic
from src.domain.bot.interfaces import IHandler
from src.domain.liabilities.use_cases.list_from_text import ListLiabilitiesFromText


class LiabilityHistoryHandler(IHandler):
    def __init__(self, list_liabilities_from_text: ListLiabilitiesFromText):
        self.list_liabilities_from_text = list_liabilities_from_text

    async def __call__(self, update: Update, user: User) -> str:
        result = "`История долгов`:\n\n"
        input_message = update.message.text
        liabilities: list[LiabilityPublic] = await self.list_liabilities_from_text(
            input_message, user.id
        )

        for i, liability in enumerate(liabilities):
            result += f"{i + 1}) {liability.liability_template.name}: {liability.count}\n"

        await update.message.reply_text(
            telegramify_markdown.markdownify(result),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return result
