import logging
from textual import on
from textual.app import App, ComposeResult

from textual.widgets import Button

from app.main_window import MainWindow
from app.providers import ChatGPTProvider, FileProvider

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

    alice_id = "alice"
    random_id = "random_text"

    def compose(self) -> ComposeResult:
        yield Button("Alice", id=self.alice_id)
        yield Button("AI-generated", id=self.random_id)

    @on(Button.Pressed, f"#{alice_id}")
    def alice_button(self):
        self.push_screen(MainWindow(FileProvider("alice")))

    @on(Button.Pressed, f"#{random_id}")
    def random_button(self):
        self.push_screen(MainWindow(ChatGPTProvider()))
