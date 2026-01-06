from typing import Sequence
from venv import logger
from twitch_bot.definitions import EventHandler, EventType
from twitch_bot.plugin_managers.interface_event_dispatcher import IEventDispatcher
from twitch_bot.plugins.bot_plugin import BotPlugin


class EventDispatcher(IEventDispatcher):
    def __init__(self, bot_plugins: Sequence[BotPlugin]) -> None:
        self._event_handlers: dict[EventType, list[EventHandler]] = {}

        for plugin in bot_plugins:
            plugin_handlers = plugin.get_event_handlers()

            for event_type, event_handler in plugin_handlers.items():
                self._event_handlers.setdefault(event_type, []).append(event_handler)

    async def dispatch(self, event: EventType, *args) -> None:
        for event_handler in self._event_handlers.get(event, []):
            try:
                await event_handler(*args)
            except Exception:
                logger.exception(f"Handler failed: {event_handler}")


# 1. не паралельно работают плагины
# 2. логируется какая то хуйня , нужна норм информация
