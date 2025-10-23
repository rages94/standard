import telegramify_markdown
from telegram import Update

from src.domain.auth_link.use_cases.create import CreateAuthLink
from src.domain.bot.interfaces import IHandler
from src.data.models import User


class LoginHandler(IHandler):
    def __init__(self, create_auth_link: CreateAuthLink):
        self.create_auth_link = create_auth_link
        self.welcome_text = (
            "Q, я нормобот, краткая инструкция по функционалу:\n"
            "`Списание`: 10 подтягиваний; спиши 40 приседаний; 50 икр и 60 скручиваний\n"
            "`Запись`: 15 смертей; запиши 21 смерть;\n"
            "`История списаний`: история; последние 15 списаний; история списаний;\n"
            "`История долгов`: история долгов; последние 13 долгов; покажи историю долгов\n"
            "`История зачетов`: зачеты; последние 5 зачетов; история зачетов; покажи историю зачетов;\n"
            "`Рейтинг`: рейтинг(покажет рейтинг за последний день); покажи рейтинг; рейтинг за 5 дней;\n"
            "`Долги`: долг; покажи долг;\n\n"
            "А теперь [авторизуйся](%s)"
        )

    async def __call__(self, update: Update, user: User) -> str:
        chat_id = update.message.chat.id
        auth_link = await self.create_auth_link(chat_id)
        link = f"{config['bot_auth']['url']}?token={auth_link.id}&chat_id={chat_id}"
        await update.message.reply_text(
            telegramify_markdown.markdownify(self.welcome_text % link),
            parse_mode=ParseMode.MARKDOWN_V2
        )
        return text