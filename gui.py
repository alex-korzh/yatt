from dataclasses import dataclass
import logging
import time
from textual import on
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Input, Label, Button

logger = logging.getLogger(__name__)

LINE_LIMIT = 45
CHUNK_SIZE = 256


def wisdom():
    with open("./assets/alice-1.txt") as f:
        while content := f.read(CHUNK_SIZE):
            yield content


@dataclass
class WPM:
    started: int | None = None
    words: int = 0
    last_wpm: int = 0

    def count_wpm(self) -> int:
        if not self.started:
            return 0
        period = int(time.time()) - self.started
        if period == 0:
            return 0
        words_per_second = self.words / period
        self.last_wpm = int(words_per_second * 60)
        return self.last_wpm


class MainWindow(Screen):
    character = 0
    wpm = WPM()
    words = wisdom()
    mistakes = set()  # of positions

    accuracy_id = "accuracy"
    wpm_id = "wpm"
    main_id = "main"

    def __accuracy(self) -> int:
        """Percentage"""
        rate = len(self.mistakes) / self.character
        return 100 - int(rate * 100)

    def compose(self) -> ComposeResult:
        yield Label("WPM: ", id=self.wpm_id)
        yield Label("Accuracy: ", id=self.accuracy_id)
        yield Input(placeholder=next(self.words), id=self.main_id)

    def __update_label(self, id: str, text: str):
        self.get_child_by_id(id).update(text)

    def __update_wpm(self, new_wpm: int):
        self.__update_label(self.wpm_id, f"WPM: {new_wpm}")

    def __update_accuracy(self):
        self.__update_label(self.accuracy_id, f"Accuracy: {self.__accuracy()}")

    def __update_placeholder(self, input: Input):
        if len(input.placeholder) < LINE_LIMIT:
            try:
                input.placeholder += next(self.words)
            except StopIteration:
                pass

    def __start_timer(self):
        if not self.wpm.started:
            self.wpm.started = int(time.time())

    def __process_word_ended(self):
        self.wpm.words += 1
        new_wpm = self.wpm.count_wpm()
        if new_wpm != 0:
            self.__update_wpm(new_wpm)
        self.__update_accuracy()

    def __process_right_character(self, event: Input.Changed):
        self.character += 1
        if event.value == " ":
            self.__process_word_ended()
        event.input.value = ""
        event.input.placeholder = event.input.placeholder[1:]

    def __process_wrong_character(self, event: Input.Changed):
        self.mistakes.add(self.character)
        self.__update_accuracy()
        event.input.value = ""

    @on(Input.Changed, f"#{main_id}")
    def process_char(self, event: Input.Changed) -> None:
        if event.input.value == "":
            return
        if len(event.input.placeholder) == 0:
            self.exit("You win")
            return

        self.__update_placeholder(event.input)
        self.__start_timer()

        if event.value == event.input.placeholder[0]:
            self.__process_right_character(event)
        else:
            self.__process_wrong_character(event)


class YattUI(App[str]):
    """Main TUI"""

    CSS = """
    MainWindow {
        align: center middle;
    }
    Screen {
        align: center middle;
    }
    #main {
        width: 40;
    }
    """
    SCREENS = {"main": MainWindow}

    def compose(self) -> ComposeResult:
        yield Button("Play", id="defmode")

    @on(Button.Pressed, "#defmode")
    def menu_button(self):
        self.push_screen("main")
