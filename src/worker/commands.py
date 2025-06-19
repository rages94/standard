import sys, os

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

import asyncio

import pymorphy3

from src.containers.container import container
from src.worker.app import app


morph = pymorphy3.MorphAnalyzer()

def normalize_phrase(phrase: str) -> str:
    words = phrase.lower().split()
    normalized_words = []

    for word in words:
        norm = morph.parse(word)[0].normal_form
        normalized_words.append(norm)

    return " ".join(normalized_words)


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
def mark_uncompleted_credits() -> None:
    async def wrapper():
        uow = container.repositories.uow()
        async with uow:
            await uow.credit_repo.mark_uncompleted()
            await uow.commit()
    asyncio.run(wrapper())

@app.command()
def normalize_completed_standard() -> None:
    async def wrapper():
        uow = container.repositories.uow()
        async with uow:
            standards = await uow.standard_repo.filter(dict())
            for standard in standards:
                standard.normal_form = normalize_phrase(standard.name.split('(')[0])
                uow.standard_repo.add(standard)
            await uow.commit()
    asyncio.run(wrapper())


if __name__ == "__main__":
    app()
