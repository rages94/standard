import sys
import os

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CallbackQueryHandler

from src.containers.container import container
from src.data.models import User
from src.data.models.message import MessageCreate
from src.domain.classifier.dto.enums import TextClass
from src.worker.tasks import ping_users


config = container.config()
auth_chat_manager = container.use_cases.auth_chat_manager()
create_message = container.use_cases.create_message()
login_handler = container.use_cases.login_handler()
classifier_model = container.gateways.classifier_model()
ping_user = container.use_cases.ping_user()

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

    response = None
    chat_id = update.message.chat_id
    text_message = update.message.text
    user: User | None = await _get_user(chat_id)
    await create_message(MessageCreate(text=text_message, chat_id=chat_id, user_id=getattr(user, 'id')))

    if not user:
        response = await login_handler(update, user)
    elif text_message == 'ping_user':
        await ping_user(user.id, user.telegram_chat_id)
    elif text_message == 'меню':
        response = 'Меню'
        await update.message.reply_text(
            response,
            reply_markup=_build_menu_keyboard(),
        )
    else:
        # TODO training ner model + распознавать текстовые числа + день/неделя/месяц
        predictions = classifier_model.predict([text_message])

        handler_func = handler_mapping.get(predictions[0])
        response = await handler_func(update, user)

    if response:
        await create_message(MessageCreate(text=response, chat_id=chat_id))

def _build_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("Долг", callback_data="total_liabilities")],
        [InlineKeyboardButton("Записать долг", callback_data="liability")],
        [InlineKeyboardButton("Списать долг", callback_data="completed_standards")],
        [InlineKeyboardButton("История списаний", callback_data="standard_history")],
        [InlineKeyboardButton("История долгов", callback_data="liability_history")],
        [InlineKeyboardButton("История зачетов", callback_data="credit_history")],
        [InlineKeyboardButton("Рейтинг", callback_data="rating")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def _get_user(chat_id: int) -> User | None:
    return await auth_chat_manager.get_auth_user(chat_id)


def _build_completed_standard_keyboard():
    return InlineKeyboardMarkup([])  # TODO


def _build_liability_keyboard():
    return InlineKeyboardMarkup([])  # TODO


async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query  # TODO rewrite on /menu

    chat_id = query.message.chat.id
    user: User | None = await _get_user(chat_id)
    await query.answer()
    handler_func = handler_mapping.get(query.data)
    if query.data == TextClass.completed_standards.value:
        completed_standard_keyboard = _build_completed_standard_keyboard()
        response = 'Выбери упражнение:'
        await query.edit_message_text(
            response,
            reply_markup=completed_standard_keyboard,
        )
    elif query.data == TextClass.liability.value:
        liability_keyboard = _build_liability_keyboard()
        response = 'Выбери долг:"'
        await query.edit_message_text(
            response,
            reply_markup=liability_keyboard,
        )
    else:
        response = await handler_func(query, user)

    if response:
        await create_message(MessageCreate(text=response, chat_id=chat_id))

def main() -> None:
    container.init_resources()
    application = Application.builder().token(container.config()["telegram"]["token"]).build()
    application.add_handler(MessageHandler(filters.ALL, conversation))
    application.add_handler(CallbackQueryHandler(menu_handler))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
