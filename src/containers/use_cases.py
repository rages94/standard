from dependency_injector import containers, providers



class UseCasesContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    repositories = providers.DependenciesContainer()
    gateways = providers.DependenciesContainer()
