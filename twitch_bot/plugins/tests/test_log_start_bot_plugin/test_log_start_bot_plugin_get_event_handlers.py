import unittest

from twitch_bot.plugins.log_start_bot_plugin import LogStartBotPlugin
from twitch_bot.definitions import EventType


class TestLogStartBotPluginGetEventHandlers(unittest.TestCase):
    def setUp(self):
        self.plugin = LogStartBotPlugin()

    def test__result__contains_ready_event(self) -> None:
        handlers = self.plugin.get_event_handlers()

        self.assertIn(EventType.READY, handlers)

    def test__ready_event_handler__callable_and_has_right_name(self) -> None:
        handlers = self.plugin.get_event_handlers()

        self.assertTrue(callable(handlers[EventType.READY]))
        self.assertEqual(
            handlers[EventType.READY].__name__, self.plugin._on_ready.__name__
        )
