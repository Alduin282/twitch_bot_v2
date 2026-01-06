from enum import Enum
from typing import Callable, Awaitable


class EventType(Enum):
    READY = "ready"
    MESSAGE = "message"


EVENT_HANDLER = Callable[..., Awaitable[None]]
