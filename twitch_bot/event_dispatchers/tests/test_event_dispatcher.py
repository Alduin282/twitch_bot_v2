from typing import Any
from unittest import IsolatedAsyncioTestCase

from twitch_bot.event_dispatchers.event_dispatcher import EventDispatcher
from twitch_bot.definitions import EventType
from twitch_bot.plugins.bot_plugin import BotPlugin


class TestPlugin(BotPlugin):
    def __init__(self):
        self.ready_called = False
        self.message_called_with = []
        self.raise_error = False
        self.error_logged = False

    def get_event_handlers(self):
        return {
            EventType.READY: self.on_ready,
            EventType.MESSAGE: self.on_message,
        }

    async def on_ready(self, bot: Any):
        if self.raise_error:
            raise ValueError("value_error_test")
        self.ready_called = True

    async def on_message(self, bot: Any, message: str):
        if self.raise_error:
            raise RuntimeError("runtime_error_test")
        self.message_called_with.append(message)


class TestEventDispatcher(IsolatedAsyncioTestCase):

    async def test__dispatch_ready__calls_plugin(self):
        plugin = TestPlugin()
        dispatcher = EventDispatcher([plugin])

        await dispatcher.dispatch(EventType.READY, "bot")
        assert plugin.ready_called is True

    async def test__dispatch_message__calls_plugin(self):
        plugin = TestPlugin()
        dispatcher = EventDispatcher([plugin])

        message = "message"
        await dispatcher.dispatch(EventType.MESSAGE, "bot", message)
        assert plugin.message_called_with == [message]

    async def test__dispatch_with_multiple_plugins__all_plugin_events_dispatched(self):
        plugin1 = TestPlugin()
        plugin2 = TestPlugin()
        dispatcher = EventDispatcher([plugin1, plugin2])

        await dispatcher.dispatch(EventType.READY, "bot")

        assert plugin1.ready_called is True
        assert plugin2.ready_called is True

    async def test__dispatch_plugin_with_exception__does_not_stop_others(self):
        plugin1 = TestPlugin()
        plugin1.raise_error = True
        plugin2 = TestPlugin()

        dispatcher = EventDispatcher([plugin1, plugin2])

        await dispatcher.dispatch(EventType.READY, "bot")

        assert plugin2.ready_called is True

    async def test__dispatch_no_handlers_does__not_fail(self):
        dispatcher = EventDispatcher([])

        await dispatcher.dispatch(EventType.READY, "bot")

    async def test__dispatch_multiple_event_types__not_fail(self):
        plugin = TestPlugin()
        dispatcher = EventDispatcher([plugin])

        message = "message"
        await dispatcher.dispatch(EventType.MESSAGE, "bot", message)
        assert plugin.message_called_with == [message]

        await dispatcher.dispatch(EventType.READY, "bot")
        assert plugin.ready_called is True
