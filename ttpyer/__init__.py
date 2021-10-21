__version__ = "0.1.0"

from .widgets import WordWidget, EndScreenWidget
from .modes import Mode, RandomWordMode, TimedMode, QuoteMode
from .typer import Typer, TimedTyper
from .cli import run, cli
