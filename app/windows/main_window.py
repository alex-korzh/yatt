import logging
from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Input, Label

from app.config import config
from app.model import Model
from app.providers import Provider


logger = logging.getLogger(__name__)


class MainWindow(Screen):
    accuracy_id = "accuracy"
    wpm_id = "wpm"
    main_id = "main"

    BINDINGS = [
        ("ctrl+b", "dismiss"),
    ]

    def __init__(
        self,
        provider: Provider,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        self.words = provider.provide()
        self.model = Model()
        super().__init__(name, id, classes)


    def compose(self) -> ComposeResult:
        yield Label("WPM: ", id=self.wpm_id)
        yield Label("Accuracy: ", id=self.accuracy_id)
        yield Input(placeholder=next(self.words), id=self.main_id)

    def __update_label(self, id: str, text: str):
        self.get_child_by_id(id).update(text)

    def __update_wpm(self, new_wpm: int):
        self.__update_label(self.wpm_id, f"WPM: {new_wpm}")

    def __update_accuracy(self, new_accuracy: int):
        self.__update_label(self.accuracy_id, f"Accuracy: {new_accuracy}")

    def __update_placeholder(self, input: Input):
        if len(input.placeholder) < config.line_limit:
            try:
                input.placeholder += next(self.words)
            except StopIteration:
                pass

    def __process_right_character(self, event: Input.Changed):
        self.model.character_typed()
        event.input.value = ""
        event.input.placeholder = event.input.placeholder[1:]

    def __process_wrong_character(self, event: Input.Changed):
        self.model.add_mistake()
        event.input.value = ""

    @on(Input.Changed, f"#{main_id}")
    def process_char(self, event: Input.Changed) -> None:
        if event.input.value == "":
            return
        if len(event.input.placeholder) == 0:
            self.dismiss("You win")
            return

        self.__update_placeholder(event.input)
        self.model.start_timer()

        if event.value == event.input.placeholder[0]:
            self.__process_right_character(event)
        else:
            self.__process_wrong_character(event)

        self.__update_accuracy(self.model.accuracy)
        self.__update_wpm(self.model.wpm)

