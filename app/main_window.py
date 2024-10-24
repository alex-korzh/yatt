import time
from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Input, Label

from app.constants import LINE_LIMIT
from app.providers import Provider
from app.wpm import WPM


class MainWindow(Screen):
    character = 0
    wpm = WPM()
    mistakes = set()  # of positions

    accuracy_id = "accuracy"
    wpm_id = "wpm"
    main_id = "main"

    def __init__(
        self,
        provider: Provider,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        self.words = provider.provide()
        super().__init__(name, id, classes)

    def __accuracy(self) -> int:
        """Percentage"""
        rate = len(self.mistakes) / self.character
        return int(100 - rate * 100)

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
            self.parent.exit("You win")
            return

        self.__update_placeholder(event.input)
        self.__start_timer()

        if event.value == event.input.placeholder[0]:
            self.__process_right_character(event)
        else:
            self.__process_wrong_character(event)
