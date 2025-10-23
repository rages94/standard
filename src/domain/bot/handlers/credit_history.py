import telegramify_markdown
from telegram import Update
from telegram.constants import ParseMode

from src.data.models import User
from src.data.models.credit import CreditPublic
from src.domain.bot.interfaces import IHandler
from src.domain.credits.use_cases.list_from_text import ListCreditsFromText


class CreditHistoryHandler(IHandler):
    def __init__(self, list_credits_from_text: ListCreditsFromText):
        self.list_credits_from_text = list_credits_from_text

    async def __call__(self, update: Update, user: User) -> str:
        status_mapping = {None: "в процессе", False: "завален", True: "выполнен"}
        result = "`История зачетов`:\n\n"
        input_message = update.message.text
        credits: list[CreditPublic] = await self.list_credits_from_text(
            input_message, user.id
        )

        for i, credit in enumerate(credits):
            result += (
                f"{i + 1}) {credit.completed_count}/{credit.count} н. "
                f"c {credit.created_at.strftime('%d.%m.%Y')} по {credit.deadline_date.strftime('%d.%m.%Y')} "
                f"({status_mapping[credit.completed]})\n"
            )

        await update.message.reply_text(
            telegramify_markdown.markdownify(result),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return result
