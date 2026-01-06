from abc import ABC, abstractmethod
from typing import Callable

from twitch_bot.definitions import EventType


class BotPlugin(ABC):
    @abstractmethod
    def get_event_handlers(self) -> dict[EventType, Callable]: ...
