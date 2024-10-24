import logging
from textual import on
from textual.app import App, ComposeResult

from textual.widgets import Button

from app.main_window import MainWindow

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
    SCREENS = {"main": MainWindow}

    defmode_id = "defmode"

    def compose(self) -> ComposeResult:
        yield Button("Play", id=self.defmode_id)

    @on(Button.Pressed, f"#{defmode_id}")
    def menu_button(self):
        self.push_screen("main")
