from abc import ABC, abstractmethod
from twitch_bot.definitions import EVENT_HANDLER, EventType


class BotPlugin(ABC):
    @abstractmethod
    def get_event_handlers(self) -> dict[EventType, EVENT_HANDLER]: ...
