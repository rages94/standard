from telegram import Bot


class BotSendMessage:
    def __init__(self, telegram_client: Bot):
        self.telegram_client = telegram_client

    async def __call__(self, text: str, chat_id: int) -> None:
        await self.telegram_client.send_message(chat_id, text, reply_markup=None)
