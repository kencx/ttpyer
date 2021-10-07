import sys
import argparse
import pytest

from ttpyer import cli


class TestParser:
    def test_number_arg(self):
        parser = cli(["--number", "50"])
        assert parser.num == 50

    def test_n_arg(self):
        parser = cli(["-n", "50"])
        assert parser.num == 50

    def test_invalid_number_arg(self):
        with pytest.raises(SystemExit) as e:
            parser = cli(["-n", "0"])
            assert isinstance(e.__context__, argparse.ArgumentTypeError)
            assert pytest.capsys.readouterr() == (
                "ttpyer [-h] [-n NUM] [--quote] [-t TIME] [-c]\n",
                "ttpyer: error: Invalid value",
            )

    def test_controls_true(self):
        parser = cli(["-c"])
        assert parser.controls == True

    def test_number_mode(self):
        parser = cli(["-n", "100"])
        assert parser.num == 100
        assert parser.controls == False
        assert parser.quote == False

    @pytest.mark.skip("not implemented yet")
    def test_timed_mode(self):
        parser = cli(["-t", "30"])
        assert parser.time == "30"

    @pytest.mark.skip("not implemented yet")
    def test_quote_mode(self):
        parser = cli(["--quote"])
        assert parser.quote == True

    def test_invalid_input(self):
        with pytest.raises(SystemExit) as e:
            parser = cli(["this is an invalid input"])
            assert isinstance(e.__context__, argparse.ArgumentError)

    def test_no_input(self):
        with pytest.raises(SystemExit) as e:
            parser = cli([""])
            assert isinstance(e.__context__, argparse.ArgumentError)
