import logging

from urwid import (
    MainLoop,
    Widget,
    Text,
    Pile,
    Filler,
    Padding,
    register_signal,
    emit_signal,
    connect_signal,
)
from urwid.main_loop import ExitMainLoop

from ttpyer import WordWidget, EndScreenWidget
from ttpyer import Mode, RandomWordMode, TimedMode

logging.basicConfig(
    filename="log.txt",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)


class Typer:

    """Class that runs the main event loop

    mode (Mode): Test mode
    words (List[str]): List of words
    show_timer (bool): Show timer if timed mode
    timer (float): TimedMode: Seconds remaining on timer; WordMode: Seconds passed
    palette (List[(name, fg, bg]): Defines colors/theme for widgets
    word_widget (WordWidget): Widget that renders the given words
    loop (MainLoop): Main event loop to be ran
    """

    def __init__(self, mode: Mode) -> None:
        self.mode = mode
        self.words = mode.words

        self.palette = [
            ("dimmed", "dark gray", ""),
            ("cursor", "black", "white"),
            ("correct", "white", ""),
            ("wrong", "light red, standout", ""),
        ]

        self.show_timer = False
        self.timer = 0
        self.word_widget = WordWidget(self.words)
        self.header = Text("", align="left")

        self.loop = MainLoop(
            self.draw_ui(), palette=self.palette, input_filter=self.input_filter
        )

        # only start timer when first key is pressed
        connect_signal(self.word_widget, "start", self.update_timer)
        connect_signal(self.word_widget, "end", self.draw_end_screen)

    def update_timer(self, loop=None, data=None) -> None:
        """Renders timer every second"""
        if not self.show_timer:
            return

        # TODO consider counting up in word mode
        if self.timer < self.mode.time:
            self.timer += 1

        self.loop.widget = self.draw_ui()
        self.alarm = self.loop.set_alarm_in(1, self.update_timer)

    def draw_ui(self) -> Padding:
        """Draws the application UI."""

        if self.show_timer:
            self.draw_header()
            pile = Pile([self.header, self.word_widget], focus_item=self.word_widget)
            return self._wrap_filler_and_padding(pile)

        else:
            return self._wrap_filler_and_padding(self.word_widget)

    def draw_header(self):
        """Draws the header with real time stats"""

        # Consider extensibility of other real time stats
        self.header.set_text(f"{str(self.timer)}")

    def draw_end_screen(self, time_taken: float, num_of_words: int) -> None:
        end_screen = EndScreenWidget(time_taken, num_of_words)
        self.loop.widget = self._wrap_filler_and_padding(end_screen)

    def _wrap_filler_and_padding(self, widget: Widget) -> Padding:
        fill = Filler(widget, valign="middle", min_height=5)
        padding = Padding(fill, align="center", width=("relative", 70))
        return padding

    def input_filter(self, keys, raw):
        """Filters for keys that perform specific key functions"""
        if "esc" in keys:
            raise ExitMainLoop()

        if "tab" in keys:
            self.reset()

        return keys

    def reset(self) -> None:
        """Resets the test by:
        - Resetting the timer
        - Resampling for new words
        """
        self.timer = self.mode.time

        new_mode = self.mode.__class__
        mode = new_mode()
        self.word_widget = WordWidget(
            mode.sample_words(self.mode.limit)
        )  # swap out with resample_words()

        self.loop.widget = self.draw_ui()

    def start(self) -> None:
        try:
            self.loop.run()

        except BaseException as e:
            logger.error(e, exc_info=True)


class TimedTyper(Typer):
    def __init__(self, mode: Mode) -> None:

        super().__init__(mode)
        self.show_timer = True
        self.timer = self.mode.time
        self.word_widget = WordWidget(self.words, self.timer)

        register_signal(Text, "end")
        connect_signal(self.word_widget, "start", self.update_timer)
        connect_signal(self.header, "end", self.draw_end_screen)

    # BUG: first keypress starts timer but does not type the char
    def update_timer(self, loop=None, data=None) -> None:

        if self.timer <= 0:
            emit_signal(self.header, "end", self.mode.time, len(self.word_widget.words))
            return
        self.timer -= 1

        self.loop.widget = super().draw_ui()
        self.alarm = self.loop.set_alarm_in(1, self.update_timer)

    def reset(self) -> None:
        new_mode = self.mode.__class__
        mode = new_mode(self.mode.time)
        self.word_widget = WordWidget(
            mode.sample_words(self.mode.limit), self.mode.time
        )
        self.loop.widget = super().draw_ui()

