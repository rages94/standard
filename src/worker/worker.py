from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import telegramify_markdown

from src.containers.container import container
from src.data.models import User
from src.domain.classifier.dto.enums import TextClass


# mapping_classifier = {
#     TextClass.completed_standards: container.use_cases.create_completed_standards_from_text(),
# }
config = container.config()
create_completed_standards_from_text = container.use_cases.create_completed_standards_from_text()
create_liabilities_from_text = container.use_cases.create_liabilities_from_text()
auth_chat_manager = container.use_cases.auth_chat_manager()
create_auth_link = container.use_cases.create_auth_link()

async def conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat.id
    user: User = await auth_chat_manager.get_auth_user(chat_id)
    if not user:
        auth_link = await create_auth_link(chat_id)
        await update.message.reply_text(
            telegramify_markdown.markdownify(
                f"Ну-ка [авторизуйся]({config['bot_auth']['url']}?token={auth_link.id}&chat_id={chat_id})"
            ),
            parse_mode=ParseMode.MARKDOWN_V2
        )
        return

    # TODO training ner model + распознавать текстовые числа
    # TODO classification
    input_message = update.message.text

    classifier_model = container.gateways.classifier_model()
    predictions = classifier_model.predict([input_message])
    if predictions[0] == TextClass.completed_standards.value:
        created_standards = await create_completed_standards_from_text(
            input_message, user.id, user.completed_type
        )
        result = (
            ("Списываю:\n" + "\n".join((f"{k}: {v}" for k, v in created_standards.items())))
            if created_standards
            else "Нифига не понял, что списать?"
        )
        await update.message.reply_text(result)
    elif predictions[0] == TextClass.liability.value:
        created_liabilities = await create_liabilities_from_text(  # TODO training on liabilities, check
            input_message, user.id
        )
        result = (
            ("Записываю:\n" + "\n".join((f"{k}: {v}" for k, v in created_liabilities.items())))
            if created_liabilities
            else "Нифига не понял, что записать?"
        )
        await update.message.reply_text(result)


def main() -> None:
    container.init_resources()
    application = Application.builder().token(container.config()["telegram"]["token"]).build()
    application.add_handler(MessageHandler(filters.ALL, conversation))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
