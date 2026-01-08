import asyncio
from dataclasses import dataclass
import random
import time


class Cooldown:
    def __init__(self, duration_seconds: float):
        self._duration = duration_seconds
        self._last_trigger_time = 0.0

    def is_ready(self) -> bool:
        return (time.time() - self._last_trigger_time) >= self._duration

    def trigger(self):
        self._last_trigger_time = time.time()


@dataclass
class Delay:
    min_seconds: float = 0.0
    max_seconds: float = 0.0

    def __post_init__(self):
        if self.min_seconds > self.max_seconds:
            raise ValueError(
                f"Delay(min_seconds={self.min_seconds}, "
                f"max_seconds={self.max_seconds}) "
                f"is invalid: min_seconds cannot be greater than max_seconds"
            )

    def should_delay(self) -> bool:
        return self.max_seconds > 0

    async def wait(self) -> None:
        await asyncio.sleep(random.uniform(self.min_seconds, self.max_seconds))
