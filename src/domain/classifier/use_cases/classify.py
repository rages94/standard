from src.domain.classifier.dto.enums import TextClass


class Classify:
    def __init__(self, classifier_model):
        self.classifier_model = classifier_model

    def __call__(self, text: str) -> TextClass:
        predictions = self.classifier_model.predict([text])
        return getattr(TextClass, predictions[0])
