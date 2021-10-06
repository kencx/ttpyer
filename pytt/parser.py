import sys
import argparse

from pytt.typer import Typer
from pytt.modes import RandomWordMode, TimedMode


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

    # display help when no arguments given
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args(args)


def main():
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


if __name__ == "__main__":
    main()
