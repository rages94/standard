from dependency_injector import containers, providers

from src.domain.classifier.use_cases.classify import Classify
from src.domain.completed_standards.use_cases.create import CreateCompletedStandard
from src.domain.completed_standards.use_cases.create_from_text import CreateCompletedStandardsFromText
from src.domain.ner.use_cases.normalize_phrase import NormalizePhrase
from src.domain.ner.use_cases.parse_standards import ParseStandards


class UseCasesContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    repositories = providers.DependenciesContainer()
    gateways = providers.DependenciesContainer()

    normalize_phrase = providers.Singleton(NormalizePhrase)
    classify = providers.Factory(
        Classify,
        classifier_model=gateways.classifier_model,
    )
    parse_standards = providers.Factory(
        ParseStandards,
        ner_model=gateways.ner_model,
        uow=repositories.uow,
        normalize_phrase=normalize_phrase,
    )
    create_completed_standards = providers.Factory(CreateCompletedStandard, uow=repositories.uow)
    create_completed_standards_from_text = providers.Factory(
        CreateCompletedStandardsFromText,
        parse_standards=parse_standards,
        create_completed_standards=create_completed_standards,
    )
