import json
from random import sample


class Mode:
    """Parent Mode class.

    word_bank ({word: count}): Dictionary of all words in given json file
    limit: word limit
    words: randomly sampled words from word_bank
    """

    def __init__(self, filename="words/english1000.json", limit=100) -> None:

        with open(filename, "r") as f:
            self.word_bank = json.load(f).keys()

        if limit <= 0:
            raise AttributeError("Invalid limit.")
        self.limit = limit

        self.words = self.sample_words(self.limit)

    def sample_words(self, limit: int) -> str:

        try:
            return " ".join(sample(list(self.word_bank), limit))

        except ValueError as e:
            raise ValueError("Limit exceeded number of available words.") from e

    def resample_words(self) -> str:  # TODO: need to test
        self.words = self.sample_words(self.limit)


class RandomWordMode(Mode):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class TimedMode(Mode):
    def __init__(self, time, **kwargs) -> None:
        super().__init__(**kwargs)
        self.time = time


class QuoteMode(Mode):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
