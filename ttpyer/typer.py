import logging

from urwid import MainLoop, Text, Filler, WidgetWrap
from urwid.main_loop import ExitMainLoop

from ttpyer import Mode, RandomWordMode, TimedMode

logging.basicConfig(
    filename="log.txt",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)


# custom widget wrapping
# https://stackoverflow.com/questions/49241164/preferred-method-to-dynamically-change-the-urwid-mainloop-widget
class WordWidget(WidgetWrap):
    def __init__(self, initial_text):
        self.text = initial_text

        self.text_widget = Text(self.text, align="center")
        super(WordWidget, self).__init__(self.text_widget)

    def update(self, new_text):
        self.text_widget.set_text(new_text)


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

        # appended empty string allows cursor to be moved to the last character (temp workaround)
        self.letters = [char for char in self.words] + [""]
        self.cursor_pos = 0
        self.input = []

        # attr wrapping
        # consider implementing custom widget https://stackoverflow.com/questions/46876041/parts-of-text-in-bold-in-urwid
        self.output = []
        for c in self.letters.copy():
            self.output.append(("dimmed", u"%s" % c))
        self.output[self.cursor_pos] = ("cursor", u"%s" % self.cursor_char)

        self.word_widget = WordWidget(self.output)
        self.typing_widget = Filler(self.word_widget)

    @property
    def cursor_char(self) -> str:
        return self.letters[self.cursor_pos]

    def update_current_pos(self, new_char) -> None:
        self.output[self.cursor_pos] = new_char

    def move_cursor_left(self) -> None:
        if self.cursor_pos > 0:
            self.cursor_pos -= 1
            self.update_current_pos(("cursor", u"%s" % self.cursor_char))

    def move_cursor_right(self) -> None:
        self.cursor_pos += 1

        if self.cursor_pos < len(self.letters) - 1:
            self.update_current_pos(("cursor", u"%s" % self.cursor_char))

    def type_char(self, keypress) -> None:
        self.input.append(keypress)  # for getting wrong chars

        current_pos = self.term.strip_seqs(self.output[self.cursor_pos])

        if keypress == current_pos:
            current_pos = ("correct", u"%s" % current_pos)
        else:
            current_pos = ("wrong", u"%s" % current_pos)

        self.update_current_pos(current_pos)

    def startScreen(self) -> None:
        pass
        # print(self.term.center(text="Press any key to start"))

    def endScreen(self) -> None:
        print(self.term.center("Press q to quit"))

        if self.term.inkey() == "q":
            self.shutdown()

    def restart(self, key):
        """Restart test if user presses Tab"""
        if key in ("tab"):
            pass

    def shutdown(self, key):
        """Exit if user presses Esc"""
        if key in ("esc"):
            raise ExitMainLoop()

    def start(self) -> None:

        try:
            loop = MainLoop(
                self.typing_widget, palette=self.palette, unhandled_input=self.shutdown
            )
            loop.run()

        except BaseException as e:
            logger.error(e)
        #     while self.cursor_pos < len(self.letters) - 1:
        #         keypress = self.term.inkey(timeout=0.05)

        #         if keypress and not keypress.is_sequence:
        #             self.type_char(keypress)
        #             self.move_cursor_right()

        #             print(self.term.move_y(self.term.height // 2))
        #             print(self.term.center(self._parse_output()))

        #         else:
        #             continue

        #     self.endScreen()


def main():
    typer = Typer(RandomWordMode())
    typer.start()


if __name__ == "__main__":
    main()
