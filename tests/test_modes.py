import pytest

from pytt.modes import Mode, RandomWordMode


@pytest.fixture
def word_file():
    return "words/english1000.json"


class TestMode:
    def test_import_word_bank(self, word_file):
        rwm = Mode(word_file)
        assert len(rwm.word_bank)

    def test_default_word_limit(self, word_file):
        rwm = RandomWordMode(word_file)
        assert len(rwm.words.split(" ")) == 10

    def test_custom_word_limit(self, word_file):
        limit = 100
        rwm = RandomWordMode(word_file, limit=limit)
        assert len(rwm.words.split(" ")) == limit

    def test_exceed_word_limit(self, word_file):
        limit = 10000
        with pytest.raises(ValueError) as excinfo:
            rwm = RandomWordMode(word_file, limit=limit)
            assert excinfo.value.message == (
                "Limit exceeded number of available words.",
            )

    def test_invalid_input_limit(self, word_file):
        limit = -1
        with pytest.raises(AttributeError) as excinfo:
            rwm = RandomWordMode(word_file, limit=limit)
            assert excinfo.value.message == ("Invalid limit.")
