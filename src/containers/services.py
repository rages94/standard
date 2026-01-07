from dependency_injector import containers, providers

from src.domain.math.services.normalization import ExerciseNormalizationService


class ServicesContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    gateways = providers.DependenciesContainer()
    repositories = providers.DependenciesContainer()

    exercise_normalization = providers.Factory(ExerciseNormalizationService)