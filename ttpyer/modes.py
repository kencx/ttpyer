import json
from random import sample


class Mode:
    def __init__(self, filename, limit=100):

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
    def __init__(self, filename="words/english1000.json", limit=10):

        super().__init__(filename, limit)


class TimedMode(Mode):
    def __init__(self, filename, time):

        super().__init__(filename)
        self.time = time
