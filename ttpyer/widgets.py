import logging

from urwid import Text, WidgetWrap
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

    def __init__(self, words):
        self.words = words

        # appended empty string allows cursor to be moved to the last character (temp workaround)
        self.letters = [char for char in self.words] + [""]
        self.cursor_pos = 0
        self.input = []

        # list of chars with attr wrapping -> [("attr", u"word"), ...]
        self.output = list(map(lambda x: ("dimmed", u"%s" % x), self.letters.copy()))
        self.output[self.cursor_pos] = ("cursor", u"%s" % self.cursor_char)

        self.text_widget = Text(self.output, align="center")
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
        A key map is defined to distinguish between hotkeys and typed characters"""

        # -2 allows test to autocomplete when last character is typed
        if self.cursor_pos < len(self.letters) - 2:
            key_map = {"esc": 1, "backspace": 2, "tab": 3}

            if key == "backspace":
                pass

            if key not in key_map:
                logger.debug(key)
                self.type_char(key)
                self.move_cursor_right()
                self.update(self.output)

        else:
            self.draw_end_screen(key)

    def update_current_pos(self, new_char) -> None:
        """Updates the character that is on the cursor's current position"""
        self.output[self.cursor_pos] = new_char

    def move_cursor_left(self) -> None:
        """Move the cursor 1 character to the left"""
        if self.cursor_pos > 0:
            self.cursor_pos -= 1
            self.update_current_pos(("cursor", u"%s" % self.cursor_char))

    def move_cursor_right(self) -> None:
        """Moves the cursor 1 character to the right."""
        self.cursor_pos += 1

        if self.cursor_pos < len(self.letters) - 1:
            self.update_current_pos(("cursor", u"%s" % self.cursor_char))

    def type_char(self, keypress) -> None:
        """Colors the current char with the appropriate color, depending on the key input

        If correct, the default color is printed. Otherwise, a red standout color is printed.
        The input is also recorded in self.input for future use.
        """

        self.input.append(keypress)  # for getting wrong chars
        current_pos = self.output[self.cursor_pos][1]

        if keypress == current_pos:
            current_pos = ("correct", u"%s" % current_pos)
        else:
            current_pos = ("wrong", u"%s" % current_pos)

        self.update_current_pos(current_pos)

    def draw_end_screen(self, key) -> None:
        """Draws the end result screen.
        Will include results such as:
            - WPM, timing, error rate
        """

        if key == "q":
            raise ExitMainLoop()

        end_screen_text = """Press q to quit"""
        self.update(end_screen_text)
