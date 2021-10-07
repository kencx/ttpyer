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
    def __init__(self, mode: Mode) -> None:
        self.words = mode.words
        self.show_timer = isinstance(mode, TimedMode)

        self.palette = [
            ("dimmed", "dark gray", ""),
            ("cursor", "black", "white"),
            ("correct", "white", ""),
            ("wrong", "light red,standout", ""),
        ]

        self.word_widget = WordWidget(self.words)
        self.fill = Filler(self.word_widget)

    def restart(self, key):
        """Restart test if user presses Tab"""
        if key == "tab":
            pass

    def shutdown(self, key):
        """Exit if user presses Esc"""
        if key == "esc":
            raise ExitMainLoop()

    def start(self) -> None:

        try:
            loop = MainLoop(
                self.fill, palette=self.palette, unhandled_input=self.shutdown
            )
            loop.run()

        except BaseException as e:
            logger.error(e, exc_info=True)

    # def startScreen(self) -> None:
    #      pass

    # def endScreen(self) -> None:
    #     print(self.term.center("Press q to quit"))


if __name__ == "__main__":
    typer = Typer(RandomWordMode())
    typer.start()
