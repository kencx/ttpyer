import logging

from urwid import MainLoop, Filler
from urwid.main_loop import ExitMainLoop

from ttpyer import WordWidget
from ttpyer import Mode, RandomWordMode, TimedMode

logging.basicConfig(
    filename="log.txt",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)


class Typer:

    """Typing function that runs the main event loop

    mode (Mode): Test mode
    words (List[str]): List of words
    show_timer (bool): Show timer if timed mode
    palette (List[(name, fg, bg]): Defines colors/theme for widgets
    word_widget (WordWidget): Main widget that draws the given words
    fill (Filler): Wraps word_widget to fill console
    loop (MainLoop): Main event loop to be ran with given widgets, palette and input_filter
    """

    def __init__(self, mode: Mode) -> None:
        self.mode = mode
        self.words = mode.words
        self.show_timer = isinstance(mode, TimedMode)

        self.palette = [
            ("dimmed", "dark gray", ""),
            ("cursor", "black", "white"),
            ("correct", "white", ""),
            ("wrong", "light red, standout", ""),
        ]

        self.word_widget = WordWidget(self.words)
        self.fill = Filler(self.word_widget)
        self.loop = MainLoop(
            self.fill, palette=self.palette, input_filter=self.input_filter
        )

    def reset(self) -> None:
        new_mode = self.mode.__class__
        self.word_widget = WordWidget(
            new_mode().sample_words(self.mode.limit)
        )  # swap out with resample_words()

        self.fill = Filler(self.word_widget)
        self.loop.widget = self.fill

    def input_filter(self, keys, raw):
        if "esc" in keys:
            raise ExitMainLoop()

        if "tab" in keys:
            self.reset()

        return keys

    def start(self) -> None:
        try:
            self.loop.run()

        except BaseException as e:
            logger.error(e, exc_info=True)


if __name__ == "__main__":
    typer = Typer(RandomWordMode())
    typer.start()
