import telegramify_markdown
from telegram import Update
from telegram.constants import ParseMode

from src.data.models import User
from src.domain.bot.interfaces import IHandler
from src.domain.completed_standards.dto.output import RatingGroupedCompletedStandard
from src.domain.rating.use_cases.get_rating_from_text import GetRatingFromText


class RatingHandler(IHandler):
    def __init__(self, get_rating_from_text: GetRatingFromText):
        self.get_rating_from_text = get_rating_from_text

    async def __call__(self, update: Update, user: User) -> str:
        result = "`Рейтинг`:\n"
        input_message = update.message.text
        grouped_completed_standards: list[RatingGroupedCompletedStandard] = await self.get_rating_from_text(
            input_message, user.id
        )

        for group in grouped_completed_standards:
            result += f"\n- **{group.standard_name}**:\n"
            for user_completed_standard in group.user_ratings:
                result += (
                    f"{user_completed_standard.username}  {user_completed_standard.standards}\n"
                )

        await update.message.reply_text(
            telegramify_markdown.markdownify(result),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return result
