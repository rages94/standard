import asyncio
from decimal import Decimal

from src.containers.container import container
from src.data.models import Message
from src.data.uow import UnitOfWork
from src.worker.app import app


if __name__ == "__main__":
    app()