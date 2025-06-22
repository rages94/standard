from dependency_injector import containers, providers

from src.domain.auth_link.use_cases.create import CreateAuthLink
from src.domain.bot.use_cases.send_message import BotSendMessage
from src.domain.classifier.use_cases.classify import Classify
from src.domain.completed_standards.use_cases.create import CreateCompletedStandard
from src.domain.completed_standards.use_cases.create_from_text import CreateCompletedStandardsFromText
from src.domain.liabilities.use_cases.create import CreateLiability
from src.domain.liabilities.use_cases.create_from_text import CreateLiabilitiesFromText
from src.domain.ner.use_cases.normalize_phrase import NormalizePhrase
from src.domain.ner.use_cases.parse_standards import ParseStandards
from src.domain.ner.use_cases.parse_liability_templates import ParseLiabilityTemplates
from src.domain.user.use_cases.check_auth_chat import AuthChatManager


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
    parse_liability_templates = providers.Factory(
        ParseLiabilityTemplates,
        ner_model=gateways.ner_model,
        uow=repositories.uow,
        normalize_phrase=normalize_phrase,
    )

    create_liability = providers.Factory(CreateLiability, uow=repositories.uow)
    create_liabilities_from_text = providers.Factory(
        CreateLiabilitiesFromText,
        parse_liability_templates=parse_liability_templates,
        create_liability=create_liability,
    )

    create_completed_standard = providers.Factory(CreateCompletedStandard, uow=repositories.uow)
    create_completed_standards_from_text = providers.Factory(
        CreateCompletedStandardsFromText,
        parse_standards=parse_standards,
        create_completed_standard=create_completed_standard,
    )

    auth_chat_manager = providers.Singleton(AuthChatManager, uow=repositories.uow)
    create_auth_link = providers.Factory(CreateAuthLink, uow=repositories.uow)
    bot_send_message = providers.Factory(BotSendMessage, telegram_client=gateways.telegram_client)
