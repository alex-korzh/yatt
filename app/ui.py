import logging
from textual import on
from textual.app import App, ComposeResult

from textual.widgets import Button

from app.main_window import MainWindow
from app.providers import ChatGPTProvider, JsonFileProvider, TextFileProvider

logger = logging.getLogger(__name__)


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
    SCREENS = {
        "main": MainWindow,
    }

    alice_id = "alice"
    random_id = "random_text"
    common_id = "common_words"
    mp_id = "mp"

    def compose(self) -> ComposeResult:
        yield Button("Alice", id=self.alice_id)
        yield Button("AI-generated", id=self.random_id)
        yield Button("Common words", id=self.common_id)
        yield Button("Multiplayer", id=self.mp_id)

    @on(Button.Pressed, f"#{alice_id}")
    def alice_button(self):
        self.push_screen(MainWindow(TextFileProvider("alice")))

    @on(Button.Pressed, f"#{random_id}")
    def random_button(self):
        self.push_screen(MainWindow(ChatGPTProvider()))

    @on(Button.Pressed, f"#{common_id}")
    def common_button(self):
        self.push_screen(MainWindow(JsonFileProvider()))
