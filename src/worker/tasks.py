import asyncio
import aiocron
import requests

from src.containers.container import container
from src.domain.user.dto.filters import UserFilterSchema

TASK_LOCKS = {}
config = container.config()

def is_llm_available() -> bool:
    try:
        response = requests.get(f'http://{config["llm_model"]["host"]}/api/version')
        response.raise_for_status()
        return True
    except Exception:
        return False

def create_cron_task(cron_expr: str):
    """Декоратор для создания cron-задачи с блокировкой и повторной попыткой."""
    def decorator(func):
        lock = asyncio.Lock()
        TASK_LOCKS[func.__name__] = lock

        @aiocron.crontab(cron_expr, start=True)
        async def wrapper():
            if lock.locked():
                print(f"{func.__name__} уже выполняется, пропускаем запуск")
                return

            async with lock:
                while True:
                    if is_llm_available():
                        print(f"{func.__name__}: сервер доступен — выполняем задачу")
                        await func()
                        break
                    else:
                        print(f"{func.__name__}: сервер недоступен — повтор через 20 минут")
                        await asyncio.sleep(20 * 60)

        return wrapper
    return decorator

@create_cron_task('0 8 */3 * *')
async def ping_users():
    list_users = container.use_cases.list_users()
    ping_user = container.use_cases.ping_user()

    users = await list_users(UserFilterSchema(chat_id_ne=None))
    for user in users:
        await ping_user(user.id, user.telegram_chat_id)
