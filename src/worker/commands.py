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


@app.command()
def _() -> None:
    pass


if __name__ == "__main__":
    app()