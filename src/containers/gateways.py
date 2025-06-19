from dependency_injector import containers, providers
import spacy
import joblib

from src.common.db import Database


class GatewaysContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    db = providers.Singleton(Database, dsn=config.database.dsn, echo=config.database.echo)
    ner_model = providers.Singleton(spacy.load, name=config.ner_model.path)
    classifier_model = providers.Singleton(joblib.load, config.classifier_model.path)
