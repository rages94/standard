import sys, os

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

import asyncio

from src.containers.container import container
from src.worker.app import app


@app.command()
def create_credits() -> None:
    async def wrapper():
        uow = container.repositories.uow()
        async with uow:
            users = await uow.user_repo.filter(dict())
            for user in users:
                if user.total_liabilities > 0:
                    await uow.credit_repo.create_by_user(user.id, user.total_liabilities)
            await uow.commit()
    asyncio.run(wrapper())

# TODO CRON
@app.command()
def mark_uncompleted_credits() -> None:
    async def wrapper():
        uow = container.repositories.uow()
        async with uow:
            await uow.credit_repo.mark_uncompleted()
            await uow.commit()
    asyncio.run(wrapper())


if __name__ == "__main__":
    app()
