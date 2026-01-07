from typing import Protocol
from twitch_bot.definitions import EventType


class IEventDispatcher(Protocol):
    async def dispatch(self, event_type: EventType, *args) -> None: ...
