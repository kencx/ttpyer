__version__ = "0.1.0"

from .widgets import WordWidget
from .modes import Mode, RandomWordMode, TimedMode
from .typer import Typer
from .cli import run, cli

if __name__ == "__main__":
    run()
