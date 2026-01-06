from enum import Enum
from typing import Callable, Awaitable


class EventType(Enum):
    READY = "ready"
    MESSAGE = "message"


EventHandler = Callable[..., Awaitable[None]]
