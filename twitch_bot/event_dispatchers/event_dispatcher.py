import asyncio
import inspect
import logging
from typing import Sequence
from twitch_bot.definitions import EVENT_HANDLER, EventType
from twitch_bot.event_dispatchers.interface_event_dispatcher import IEventDispatcher
from twitch_bot.plugins.bot_plugin import BotPlugin


logger = logging.getLogger(__name__)


class EventDispatcher(IEventDispatcher):
    def __init__(self, bot_plugins: Sequence[BotPlugin]) -> None:
        self._event_handlers: dict[EventType, list[EVENT_HANDLER]] = {}

        for plugin in bot_plugins:
            plugin_handlers = plugin.get_event_handlers()

            for event_type, event_handler in plugin_handlers.items():
                self._event_handlers.setdefault(event_type, []).append(event_handler)

    async def dispatch(self, event_type: EventType, *args) -> None:
        event_handlers = self._event_handlers.get(event_type, [])

        if not event_handlers:
            return

        handler_calls = [
            self._safe_call(event_type, handler, *args) for handler in event_handlers
        ]

        await asyncio.gather(*handler_calls, return_exceptions=True)

    async def _safe_call(
        self,
        event_type: EventType,
        event_handler: EVENT_HANDLER,
        *args,
    ) -> None:
        try:
            await event_handler(*args)
        except Exception:
            logger.exception(
                "Event handler failed",
                extra={
                    "event": event_type.value,
                    "plugin": self._get_plugin_name(event_handler),
                },
            )

    def _get_plugin_name(
        self,
        event_handler: EVENT_HANDLER,
    ):
        if inspect.ismethod(event_handler):
            return event_handler.__self__.__class__.__name__
        else:
            return "No plugin found"
