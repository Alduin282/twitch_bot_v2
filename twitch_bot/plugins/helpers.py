import time


class Cooldown:
    def __init__(self, duration_seconds: float):
        self._duration = duration_seconds
        self._last_trigger_time = 0.0

    def is_ready(self) -> bool:
        return (time.time() - self._last_trigger_time) >= self._duration

    def trigger(self):
        self._last_trigger_time = time.time()
