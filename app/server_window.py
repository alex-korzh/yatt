from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button


class ServerWindow(Screen):
    BINDINGS = [
        ("ctrl+b", "dismiss"),
    ]

    def compose(self) -> ComposeResult:
        yield Button("Connect to server")
        yield Button("Find game", disabled=True)
