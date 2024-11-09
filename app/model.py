import time


class Model:
    
    def __init__(self):
        self.character = 0
        self.mistakes = set()  # of positions
        self.started: int | None = None
        self.last_wpm: int = 0
    
    @property
    def accuracy(self) -> int:
        """Percentage"""
        if self.character == 0:
            return 0
        rate = len(self.mistakes) / self.character
        return int(100 - rate * 100)

    def add_mistake(self) -> None:
        self.mistakes.add(self.character)
        
    def character_typed(self):
        self.character += 1

    @property    
    def wpm(self):
        return self.count_wpm()

    def count_wpm(self) -> int:
        if not self.started:
            return 0
        period = int(time.time()) - self.started
        if period == 0:
            return 0
        words = self.character / 4
        words_per_second = words / period
        self.last_wpm = int(words_per_second * 60)
        return self.last_wpm

    def start_timer(self):
        if not self.started:
            self.started = int(time.time())