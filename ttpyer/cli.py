import sys
import argparse

from ttpyer import Typer, TimedTyper
from ttpyer import RandomWordMode, TimedMode, QuoteMode


def number_check(n):
    n = int(n)
    if n <= 0:
        raise argparse.ArgumentTypeError("Invalid value")
    return n


def cli(args=None):

    parser = argparse.ArgumentParser(
        prog="ttpyer",
        description="A terminal based typing test application written in Python",
    )

    parser.add_argument(
        "-n",
        "--number",
        action="store",
        default="10",
        type=number_check,
        help="number of words",
        dest="num",
    )
    # timed quote mode?
    parser.add_argument("-t", "--time", type=int, help="time (s)")
    parser.add_argument("--quote", action="store_true", help="enable quote mode")
    parser.add_argument("-c", "--controls", action="store_true", help="show controls")

    return parser.parse_args(args)


def run():
    parser = cli(sys.argv[1:])

    if parser.controls:
        # show key bindings
        pass

    elif parser.time:
        typer = TimedTyper(TimedMode(time=int(parser.time)))
        typer.start()

    elif parser.quote:
        typer = Typer(QuoteMode())
        typer.start()

    elif parser.num:
        typer = Typer(RandomWordMode(limit=int(parser.num)))
        typer.start()
