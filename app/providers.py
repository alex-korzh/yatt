import abc
import json
import logging
import random
from typing import Iterable, Literal

from openai import OpenAI

from app.constants import CHUNK_SIZE, OPENAI_API_KEY, OPENAI_PROMPT

logger = logging.getLogger(__name__)


class Provider(abc.ABC):
    def provide(self) -> Iterable[str]:
        raise NotImplementedError


class TextFileProvider(Provider):
    def __init__(self, file: Literal["alice", "example"]) -> None:
        self.filename: str = {
            "alice": "./assets/alice-1.txt",
            "example": "./assets/example-text.txt",
        }[file]

    def provide(self) -> Iterable[str]:
        with open(self.filename) as f:
            while content := f.read(CHUNK_SIZE):
                yield content


class JsonFileProvider(Provider):
    def __init__(self) -> None:
        self.filename = "./assets/1000.json"

    def provide(self) -> Iterable[str]:
        with open(self.filename) as f:
            data = json.load(f)["words"]
            chunks = (len(data) // CHUNK_SIZE) + 1
            for i in range(0, chunks):
                yield " ".join(random.sample(data, CHUNK_SIZE))


class ChatGPTProvider(Provider):
    def __init__(self) -> None:
        if not OPENAI_API_KEY:
            raise Exception("No API key provided!")
        self.client = OpenAI()
        self.data = (
            self.client.with_options(max_retries=0)
            .chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": OPENAI_PROMPT,
                    }
                ],
            )
            .choices[0]
            .message.content
        )

    def provide(self) -> Iterable[str]:
        for i in range(0, len(self.data), CHUNK_SIZE):
            yield self.data[i : i + CHUNK_SIZE]
