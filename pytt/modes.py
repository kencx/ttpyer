import json
from random import sample
from typing import List


class Mode:
    def __init__(self, filename):

        self.limit = 100
        with open(filename, "r") as f:
            self.word_bank = json.load(f).keys()

    def sample_words(self, limit: int) -> List:
        return " ".join(sample(list(self.word_bank), limit))


class RandomWordMode(Mode):
    def __init__(self, filename="words/english1000.json", limit=10):

        super().__init__(filename)
        self.limit = limit
        self.words = self.sample_words(self.limit)


class TimedMode(Mode):
    def __init__(self, filename, time):

        super().__init__(filename)
        self.time = time
        self.words = self.sample_words(self.limit)
