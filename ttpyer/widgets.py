import logging
from urwid import Text, WidgetWrap


logging.basicConfig(
    filename="log.txt",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)


# custom widget wrapping
# https://stackoverflow.com/questions/49241164/preferred-method-to-dynamically-change-the-urwid-mainloop-widget
class WordWidget(WidgetWrap):
    def __init__(self, words):
        self.words = words

        # appended empty string allows cursor to be moved to the last character (temp workaround)
        self.letters = [char for char in self.words] + [""]
        self.cursor_pos = 0
        self.input = []

        # list of chars with attr wrapping -> [("attr", u"word"), ...]
        self.output = list(map(lambda c: ("dimmed", u"%s" % c), self.letters.copy()))
        self.output[self.cursor_pos] = ("cursor", u"%s" % self.cursor_char)

        self.text_widget = Text(self.output, align="center")
        super(WordWidget, self).__init__(self.text_widget)

    @property
    def cursor_char(self) -> str:
        return self.letters[self.cursor_pos]

    def selectable(self) -> bool:
        return True

    def update(self) -> None:
        self.text_widget.set_text(self.output)

    def keypress(self, size, key) -> None:
        if self.cursor_pos < len(self.letters) - 1:

            if key != "esc":
                logger.debug(key)
                self.type_char(key)
                self.move_cursor_right()
                self.update()

            # backspace
            # restart

        else:  # endscreen
            pass

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
        current_pos = self.output[self.cursor_pos][1]

        if keypress == current_pos:
            current_pos = ("correct", u"%s" % current_pos)
        else:
            current_pos = ("wrong", u"%s" % current_pos)

        self.update_current_pos(current_pos)
