import pymorphy3


class NormalizePhrase:
    def __init__(self):
        self.morph = pymorphy3.MorphAnalyzer()

    def __call__(self, phrase: str) -> str:
        words = phrase.lower().split()
        normalized_words = []

        for word in words:
            norm = self.morph.parse(word)[0].normal_form
            if norm == 'отжимания':
                norm = 'отжимание'
            normalized_words.append(norm)

        return " ".join(normalized_words)
