from dataclasses import dataclass
import time


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
