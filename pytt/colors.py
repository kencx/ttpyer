from blessed import Terminal
from blessed.formatters import FormattingString


class Color:
    def __init__(self) -> None:

        self.term = Terminal()

        self.GRAY = self.getColorFormat("dimgray")
        self.WHITE = self.getColorFormat("ghostwhite")
        self.RED_REVERSE = self.getColorFormat("red_reverse")
        self.BLACK_ON_WHITE = self.getColorFormat("black_on_white")

    def getColorFormat(self, color: str) -> FormattingString:
        return FormattingString(getattr(self.term, color), self.term.normal)
