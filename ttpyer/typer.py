import sys

from urwid import MainLoop, Text, Padding, Filler
from urwid.main_loop import ExitMainLoop

from ttpyer import Color
from ttpyer import Mode, RandomWordMode, TimedMode


class Typer:

    color = Color()

    def __init__(self, mode: Mode) -> None:

        self.show_timer = isinstance(mode, TimedMode)
        self.palette = [("dim", "dark gray", ""), ("cursor", "black", "white")]
        self.words = mode.words

        # appended empty string allows cursor to be moved to the last character (temp workaround)
        self.letters = [char for char in self.words] + [""]
        self.cursor_pos = 0
        self.input = []

        self.output = []
        for c in self.letters.copy():
            self.output.append(("dim", u"%s" % c))
        self.output[self.cursor_pos] = ("cursor", u"%s" % self.cursor_char)

    @property
    def cursor_char(self) -> str:
        return self.letters[self.cursor_pos]

    def update_current_pos(self, new_char) -> None:
        self.output[self.cursor_pos] = new_char

    # def _parse_output(self) -> str:
    #     return "".join(self.output)

    def _print_center_message(self) -> None:
        print(
            self.term.enter_fullscreen
            + self.term.clear
            + self.term.move_y(self.term.height // 2)
        )

    def move_cursor_left(self) -> None:
        if self.cursor_pos > 0:
            self.cursor_pos -= 1
            self.update_current_pos(self.color.BLACK_ON_WHITE(self.cursor_char))

    def move_cursor_right(self) -> None:
        self.cursor_pos += 1

        if self.cursor_pos < len(self.letters) - 1:
            self.update_current_pos(self.color.BLACK_ON_WHITE(self.cursor_char))

    def type_char(self, keypress) -> None:
        self.input.append(keypress)  # for getting wrong chars

        current_pos = self.term.strip_seqs(self.output[self.cursor_pos])

        if keypress == current_pos:
            current_pos = self.color.WHITE(current_pos)
        else:
            current_pos = self.color.RED_REVERSE(current_pos)

        self.update_current_pos(current_pos)

    def startScreen(self) -> None:
        self._print_center_message()
        # print(self.term.center(text="Press any key to start"))

    def endScreen(self) -> None:
        self._print_center_message()

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

        text = Text(self.output, align="center")
        fill = Filler(text)
        loop = MainLoop(fill, palette=self.palette, unhandled_input=self.shutdown)
        loop.run()

        #     self.startScreen()

        #     while self.cursor_pos < len(self.letters) - 1:
        #         keypress = self.term.inkey(timeout=0.05)

        #         if keypress.name == "KEY_ESCAPE":  # quit gracefully with Esc
        #             self.shutdown()

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
