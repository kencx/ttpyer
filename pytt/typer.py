import time

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
        # print(self.term.center(text="Press any key to start"))

    def _endScreen(self, duration):
        self._printCenterMessage()

        wpm = (len(self.phrase) / 5) / (duration / 60)  # verify formula

        print(self.term.center(f"WPM: {wpm}. Press q to quit"))

        if self.term.inkey() == "q":
            print(self.term.exit_fullscreen + self.term.clear)

    def start(self):

        self._startScreen()

        with self.term.cbreak(), self.term.hidden_cursor():

            char_idx = 0
            print(self.term.center(self.phrase))

            startTime = time.time()  # todo: only start timer when first key is pressed

            while char_idx < len(self.letters):
                keypress = self.term.inkey(timeout=0.5)
                char = self.letters[char_idx]

                if keypress.code == 361:  # quit gracefully with Esc
                    print(self.term.exit_fullscreen)

                if keypress and not keypress.is_sequence:

                    if keypress == char:
                        self.output[char_idx] = self._colorChar(char, True)
                    else:
                        self.output[char_idx] = self._colorChar(char, False)

                    char_idx += 1

                    print(self.term.move_y(self.term.height // 2))
                    print(self.term.center(text=self._parseOutput()))

                else:
                    continue

            endTime = time.time()
            duration = endTime - startTime
            self._endScreen(duration)


def main():
    phrase = "hello world, how are you doing"
    term = Terminal()
    typer = Typer(phrase, term)
    typer.start()


if __name__ == "__main__":
    main()
