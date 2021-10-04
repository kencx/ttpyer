from typing import List
from blessed import Terminal
from blessed.formatters import FormattingString


class Typer:
    def __init__(self, phrase: str, term: Terminal) -> None:

        self.term = term
        self.line_length = 70  # for paragraphs

        self.phrase = phrase
        self.letters = [char for char in phrase]
        self.output = self.letters.copy()

        self.GREEN = FormattingString(self.term.green, self.term.normal)
        self.RED = FormattingString(self.term.red, self.term.normal)

    def _printCenterMessage(self):
        print(
            self.term.enter_fullscreen
            + self.term.clear
            + self.term.move_y(self.term.height // 2)
        )

    def _colorChar(self, char, choice):
        return self.GREEN(char) if choice else self.RED(char)

    def _parseOutput(self):
        return "".join(self.output)

    def _startScreen(self):
        self._printCenterMessage()

    def _endScreen(self):
        self._printCenterMessage()
        print(self.term.center("Done!"))

        # on any key, exit

        print(self.term.exit_fullscreen)

    def start(self):

        # on any key, start
        self._startScreen()

        with self.term.cbreak(), self.term.hidden_cursor():

            char_idx = 0
            print(self.term.center(text=self.phrase))

            while char_idx < len(self.letters):
                keypress = self.term.inkey(timeout=0.5)
                char = self.letters[char_idx]

                if keypress:
                    if keypress == char:
                        self.output[char_idx] = self._colorChar(char, True)
                    else:
                        self.output[char_idx] = self._colorChar(char, False)

                    char_idx += 1

                    print(self.term.move_y(self.term.height // 2))
                    print(self.term.center(text=self._parseOutput()))

                else:
                    continue

            # finish screen
            self._endScreen()


def main():
    phrase = "hello world from america"
    term = Terminal()
    typer = Typer(phrase, term)
    typer.start()


if __name__ == "__main__":
    main()
