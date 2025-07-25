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
        normalize_phrase = container.use_cases.normalize_phrase()
        async with uow:
            standards = await uow.standard_repo.filter(dict())
            for standard in standards:
                standard.normal_form = normalize_phrase(standard.name.split('(')[0])
                uow.standard_repo.add(standard)
            await uow.commit()
    asyncio.run(wrapper())

@app.command()
def normalize_liability_templates() -> None:
    async def wrapper():
        uow = container.repositories.uow()
        normalize_phrase = container.use_cases.normalize_phrase()
        async with uow:
            liability_templates = await uow.liability_template_repo.filter(dict())
            for liability_template in liability_templates:
                liability_template.normal_form = normalize_phrase(liability_template.name)
                uow.liability_template_repo.add(liability_template)
            await uow.commit()
    asyncio.run(wrapper())

if __name__ == "__main__":
    app()
