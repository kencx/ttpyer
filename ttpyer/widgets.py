import time
import logging
from typing import List
from inspect import cleandoc

from urwid import Text, WidgetWrap, connect_signal, emit_signal, register_signal
from urwid.main_loop import ExitMainLoop

logging.basicConfig(
    filename="log.txt",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)


class WordWidget(WidgetWrap):

    """A custom widget defined by widget wrapping in urwid
    Refer to https://stackoverflow.com/questions/49241164/preferred-method-to-dynamically-change-the-urwid-mainloop-widget

    words (List[str]): List of words
    letters (List[str]): Combined list of characters for each word
    cursor_pos (int): Current cursor position
    input (List[str]): User key input
    output (List[(attr, ustr)]): List of characters grouped by their display attr and str. The display attr defines the colors of the str.
    text_widget: The key widget that prints the output to the console.

    @property
    cursor_char (str): The character at the current cursor_pos
    """

    def __init__(self, words: List[str], timer=0):
        self.words = words
        self.timer = timer

        # appended empty string allows cursor to be moved to the last character (temp workaround)
        self.letters = [char for char in self.words] + [""]
        self.cursor_pos = 0
        self.input = []

        self.first_key = True
        self.start_time = 0
        self.end_time = 0

        # list of chars with attr wrapping -> [("attr", u"word"), ...]
        self.output = list(map(lambda x: ("dimmed", "%s" % x), self.letters.copy()))
        self.output[self.cursor_pos] = ("cursor", "%s" % self.cursor_char)

        register_signal(self.__class__, ["start", "end"])

        self.align = "left" if len(self.letters) >= 70 else "center"
        self.text_widget = Text(self.output, align=self.align)
        super(WordWidget, self).__init__(self.text_widget)

    @property
    def cursor_char(self) -> str:
        return self.letters[self.cursor_pos]

    def selectable(self) -> bool:
        return True

    def update(self, text) -> None:
        self.text_widget.set_text(text)

    def keypress(self, size, key) -> None:
        """Handles all user keyboard input.
        A key map is defined to distinguish between hotkeys and typed characters
        """

        # len-2 allows test to autocomplete when last character is typed
        if self.cursor_pos < len(self.letters) - 2:
            key_map = {"esc": 1, "backspace": 2, "tab": 3}

            if key == "backspace" and self.cursor_pos > 0:
                self.delete_char()
                self.move_cursor_left()
                self.update(self.output)

            if key not in key_map:
                if self.first_key:
                    emit_signal(self, "start")  # emit start signal
                    self.start_time = time.time()
                    self.first_key = False

                logger.debug(key)
                self.type_char(key)
                self.move_cursor_right()
                self.update(self.output)
                # TODO: do not end test immediately if last char is wrong

        else:
            if self.end_time == 0:  # prevents time from changing
                self.end_time = time.time()
            emit_signal(self, "end", self.end_time - self.start_time, len(self.words))

    def update_current_pos(self, new_char) -> None:
        """Updates the character that is on the cursor's current position"""
        self.output[self.cursor_pos] = new_char

    def move_cursor_left(self) -> None:
        """Move the cursor 1 character to the left"""
        if self.cursor_pos > 0:
            self.cursor_pos -= 1
            self.update_current_pos(("cursor", "%s" % self.cursor_char))

    def move_cursor_right(self) -> None:
        """Moves the cursor 1 character to the right."""
        self.cursor_pos += 1

        if self.cursor_pos < len(self.letters) - 1:
            self.update_current_pos(("cursor", "%s" % self.cursor_char))

    def type_char(self, keypress) -> None:
        """Colors the current char with the appropriate color, depending on the key input

        If correct, the default color is printed. Otherwise, a red standout color is printed.
        The input is also recorded in self.input for future use.
        """

        self.input.append(keypress)  # for getting wrong chars
        current_char = self.output[self.cursor_pos][1]

        if keypress == current_char:
            current_char = ("correct", "%s" % current_char)
        else:
            current_char = ("wrong", "%s" % current_char)

        self.update_current_pos(current_char)

    def delete_char(self) -> None:

        self.input.pop()
        current_char = self.output[self.cursor_pos][1]
        current_char = ("dimmed", "%s" % current_char)
        self.update_current_pos(current_char)


class EndScreenWidget(WidgetWrap):
    def __init__(self, time_taken: float, num_of_words: int):

        self.text_widget = Text(
            self.draw_stats(time_taken, num_of_words), align="center"
        )
        super(EndScreenWidget, self).__init__(self.text_widget)

    def selectable(self) -> bool:
        return True

    def keypress(self, size, key) -> None:
        if key == "q":
            raise ExitMainLoop()

    def draw_stats(self, time_taken: float, num_of_words: int) -> str:
        """Draws the end result screen."""

        # BUG: num_of_words is default total words, should be total typed words
        wpm = (num_of_words / 5) / (time_taken / 60)

        end_screen_text = f"""
            Time: {time_taken:.2f}s
            WPM: {wpm:.2f}
            Accuracy: 0%
            Press tab to retry
            Press q to quit
        """
        return cleandoc(end_screen_text)
