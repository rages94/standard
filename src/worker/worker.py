from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import telegramify_markdown

from src.containers.container import container
from src.data.models import User
from src.data.models.completed_standard import CompletedStandardPublic
from src.domain.classifier.dto.enums import TextClass
from src.domain.completed_standards.dto.output import RatingGroupedCompletedStandard

# mapping_classifier = {
#     TextClass.completed_standards: container.use_cases.create_completed_standards_from_text(),
# }
config = container.config()
create_completed_standards_from_text = container.use_cases.create_completed_standards_from_text()
create_liabilities_from_text = container.use_cases.create_liabilities_from_text()
get_rating_from_text = container.use_cases.get_rating_from_text()
auth_chat_manager = container.use_cases.auth_chat_manager()
create_auth_link = container.use_cases.create_auth_link()
list_completed_standards_from_text = container.use_cases.list_completed_standards_from_text()
get_user = container.use_cases.get_user()
classifier_model = container.gateways.classifier_model()

async def conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user: User = await auth_chat_manager.get_auth_user(update.message.chat.id)
    if not user:
        await handle_login(update, user)
        return

    # TODO training ner model + распознавать текстовые числа
    predictions = classifier_model.predict([update.message.text])
    # TODO mapping
    if predictions[0] == TextClass.completed_standards.value:
        await handle_standard(update, user)
    elif predictions[0] == TextClass.liability.value:
        await handle_liability(update, user)
    elif predictions[0] == TextClass.rating.value:
        await handle_rating(update, user)
    elif predictions[0] == TextClass.history.value:
        await handle_history(update, user)
    elif predictions[0] == TextClass.other.value:
        await handle_other(update, user)


# TODO handlers to container
async def handle_login(update: Update, user: User) -> None:
    # TODO register
    chat_id = update.message.chat.id
    auth_link = await create_auth_link(chat_id)
    await update.message.reply_text(
        telegramify_markdown.markdownify(
            f"Ну-ка [авторизуйся]({config['bot_auth']['url']}?token={auth_link.id}&chat_id={chat_id})"
        ),
        parse_mode=ParseMode.MARKDOWN_V2
    )

async def handle_liability(update: Update, user: User) -> None:
    input_message = update.message.text
    created_liabilities = await create_liabilities_from_text(  # TODO training on liabilities, check
        input_message, user.id
    )
    user: User = await get_user(user.id)
    if created_liabilities:
        result = "Записываю:\n" + "\n".join((f"- {k}: {v}" for k, v in created_liabilities.items()))
        result += f"\n\n**Текущий долг**: {user.total_liabilities} н."
    else:
        result = "Нифига не понял, что записать?"

    await update.message.reply_text(
        telegramify_markdown.markdownify(result),
        parse_mode=ParseMode.MARKDOWN_V2
    )

async def handle_standard(update: Update, user: User) -> None:
    input_message = update.message.text
    created_standards = await create_completed_standards_from_text(
        input_message, user.id, user.completed_type
    )
    user: User = await get_user(user.id)
    if created_standards:
        result = ("Списываю:\n" + "\n".join((f"- {k}: {v}" for k, v in created_standards.items())))
        result += f"\n\n**Оставшийся долг**: {user.total_liabilities} н."
    else:
        result = "Нифига не понял, что списать?"

    await update.message.reply_text(
        telegramify_markdown.markdownify(result),
        parse_mode=ParseMode.MARKDOWN_V2
    )


async def handle_rating(update: Update, user: User) -> None:
    result = "`Рейтинг`:\n"
    input_message = update.message.text
    grouped_completed_standards: list[RatingGroupedCompletedStandard] = await get_rating_from_text(
        input_message,
        user.id,
    )
    for group in grouped_completed_standards:
        result += "\n" * bool(result) + f"- **{group.standard_name}**:\n"
        for user_completed_standard in group.user_ratings:
            result += f"{user_completed_standard.username}  {user_completed_standard.standards}\n"

    await update.message.reply_text(
        telegramify_markdown.markdownify(result),
        parse_mode=ParseMode.MARKDOWN_V2
    )

async def handle_history(update: Update, user: User) -> None:
    result = "`История списаний`:\n\n"
    input_message = update.message.text
    completed_standards: list[CompletedStandardPublic] = await list_completed_standards_from_text(
        input_message,
        user.id,
    )
    for i, completed_standard in enumerate(completed_standards):
        result += f"{i + 1}) {completed_standard.standard.name}: {completed_standard.count}\n"
    await update.message.reply_text(
        telegramify_markdown.markdownify(result),
        parse_mode=ParseMode.MARKDOWN_V2
    )

async def handle_other(update: Update, user: User) -> None:
    result = "Хоп-хей"
    await update.message.reply_text(result)


def main() -> None:
    container.init_resources()
    application = Application.builder().token(container.config()["telegram"]["token"]).build()
    application.add_handler(MessageHandler(filters.ALL, conversation))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
