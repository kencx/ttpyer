import sys
import argparse

from pytt import Typer
from pytt import RandomWordMode, TimedMode


def number_check(n):
    n = int(n)
    if n <= 0:
        raise argparse.ArgumentTypeError("Invalid value")
    return n


def cli(args=None):

    parser = argparse.ArgumentParser(
        prog="pytt",
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
    parser.add_argument("-t", "--time", default=30, type=int, help="time (s)")
    parser.add_argument("--quote", action="store_true", help="enable quote mode")
    parser.add_argument("-c", "--controls", action="store_true", help="show controls")

    return parser.parse_args(args)


def run():
    parser = cli(sys.argv[1:])

    if parser.controls:
        pass

    elif parser.num:
        typer = Typer(RandomWordMode(limit=int(parser.num)))
        typer.start()

    elif parser.time or parser.t:
        pass
        # typer = Typer(TimedMode())
        # typer.start()
