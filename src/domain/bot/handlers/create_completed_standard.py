import telegramify_markdown
from telegram import Update
from telegram.constants import ParseMode

from src.data.models import User
from src.data.uow import UnitOfWork
from src.domain.bot.interfaces import IHandler
from src.domain.completed_standards.use_cases.create_from_text import CreateCompletedStandardsFromText
from src.domain.credits.use_cases.get_active import GetActiveCredit
from src.domain.user.use_cases.get import GetUser


class CreateCompletedStandardHandler(IHandler):
    def __init__(
        self,
        create_completed_standards_from_text: CreateCompletedStandardsFromText,
        uow: UnitOfWork,
        get_active_credit: GetActiveCredit,
    ):
        self.create_completed_standards_from_text = create_completed_standards_from_text
        self.uow = uow
        self.get_active_credit = get_active_credit

    async def __call__(self, update: Update, user: User) -> str:
        input_message = update.message.text
        created_standard = await self.create_completed_standards_from_text(
            input_message, user, user.completed_type
        )

        if created_standard:
            async with self.uow:
                user = await self.uow.user_repo.get_one(dict(id=user.id))
                standard = await self.uow.standard_repo.get_one(dict(id=created_standard.standard_id))

            result = (
                "Списываю:\n" +
                f"- {standard.name}: " +
                (
                    f"{created_standard.weight} кг. x {int(created_standard.count)}, {created_standard.total_norm:.2f} норм"
                    if created_standard.weight else
                    f"{int(created_standard.count)}, {created_standard.total_norm:.2f} норм"
                )
            )
            result += f"\n\n**Оставшийся долг**: {user.total_liabilities:.2f} н."
            credit = await self.get_active_credit(user.id)
            if credit:
                result += f"\n**Оставшийся зачет**: {credit.count - credit.completed_count} н."
        else:
            result = "Нифига не понял, что списать?"

        await update.message.reply_text(
            telegramify_markdown.markdownify(result),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return result
