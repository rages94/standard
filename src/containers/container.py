from dependency_injector import containers, providers

from src.config import Settings
from src.containers.gateways import GatewaysContainer
from src.containers.repositories import RepositoriesContainer
from src.containers.use_cases import UseCasesContainer



class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(packages=["src.api.routers"])
    gateways = providers.Container(GatewaysContainer, config=config)
    repositories = providers.Container(RepositoriesContainer, config=config, gateways=gateways)
    use_cases = providers.Container(UseCasesContainer, config=config, gateways=gateways, repositories=repositories)


container = Container()
container.config.from_dict(Settings().model_dump())
