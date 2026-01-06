from abc import ABC, abstractmethod
from twitch_bot.definitions import EventHandler, EventType


class BotPlugin(ABC):
    @abstractmethod
    def get_event_handlers(self) -> dict[EventType, EventHandler]: ...
