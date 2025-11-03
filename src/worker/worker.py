import sys
import os

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

from src.containers.container import container
from src.data.models import User
from src.data.models.message import MessageCreate
from src.domain.classifier.dto.enums import TextClass


config = container.config()
auth_chat_manager = container.use_cases.auth_chat_manager()
create_message = container.use_cases.create_message()
login_handler = container.use_cases.login_handler()
classifier_model = container.gateways.classifier_model()

handler_mapping = {
    TextClass.completed_standards.value: container.use_cases.create_completed_standard_handler(),
    TextClass.liability.value: container.use_cases.create_liability_handler(),
    TextClass.rating.value: container.use_cases.rating_handler(),
    TextClass.standard_history.value: container.use_cases.standard_history_handler(),
    TextClass.liability_history.value: container.use_cases.liability_history_handler(),
    TextClass.credit_history.value: container.use_cases.credit_history_handler(),
    TextClass.total_liabilities.value: container.use_cases.total_liabilities_handler(),
    TextClass.other.value: container.use_cases.other_handler(),
}

async def conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    chat_id = update.message.chat_id
    text_message = update.message.text
    user: User | None = await auth_chat_manager.get_auth_user(chat_id)
    await create_message(MessageCreate(text=text_message, chat_id=chat_id, user_id=getattr(user, 'id')))

    if not user:
        response = await login_handler(update, user)
    else:
        # TODO training ner model + распознавать текстовые числа + день/неделя/месяц
        predictions = classifier_model.predict([text_message])

        handler_func = handler_mapping.get(predictions[0])
        response = await handler_func(update, user)

    if response:
        await create_message(MessageCreate(text=response, chat_id=chat_id))


def main() -> None:
    container.init_resources()
    application = Application.builder().token(container.config()["telegram"]["token"]).build()
    application.add_handler(MessageHandler(filters.ALL, conversation))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
