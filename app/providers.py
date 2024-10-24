import abc
from typing import Generator, Literal

from app.constants import CHUNK_SIZE


class Provider(abc.ABC):
    def provide(self) -> Generator[str, None, None]:
        raise NotImplementedError


class FileProvider(Provider):
    def __init__(self, file: Literal["alice", "example"]) -> None:
        self.filename: str = {
            "alice": "./assets/alice-1.txt",
            "example": "./assets/example-text.txt",
        }[file]

    def provide(self) -> Generator[str, None, None]:
        with open(self.filename) as f:
            while content := f.read(CHUNK_SIZE):
                yield content
