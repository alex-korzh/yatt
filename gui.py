from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Input, Label


class YattUI(App[str]):
    """Main TUI"""

    CSS = """
    Screen {
        align: center middle;
    }
    #main {
        width: 40;
    }
    """

    def compose(self) -> ComposeResult:
        yield Label("", id="message")
        yield Input(placeholder="Hello typing", id="main")

    @on(Input.Changed)
    def process_char(self, event: Input.Changed) -> None:
        if len(event.input.placeholder) == 0:
            self.exit("You win")
        else:
            if event.value == event.input.placeholder[0]:
                event.input.value = ""
                event.input.placeholder = event.input.placeholder[1:]
            else:
                event.input.value = ""
