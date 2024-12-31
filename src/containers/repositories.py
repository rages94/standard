from dependency_injector import containers, providers

from src.data.uow import UnitOfWork


class RepositoriesContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    gateways = providers.DependenciesContainer()
    uow = providers.Singleton(UnitOfWork, db=gateways.db)