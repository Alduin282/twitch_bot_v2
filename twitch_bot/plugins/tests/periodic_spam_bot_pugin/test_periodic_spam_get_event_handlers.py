import unittest

from twitch_bot.plugins.periodic_spam_bot_plugin import PeriodicSpamBotPlugin
from twitch_bot.plugins.helpers import DurationRange
from twitch_bot.definitions import EventType


class TestPeriodicSpamBotPluginGetEventHandlers(unittest.TestCase):

    def setUp(self):
        self.plugin = PeriodicSpamBotPlugin(
            messages=["test_message"],
            interval=DurationRange(1.0, 2.0),
        )

    def test__result__contains_message_event(self):
        handlers = self.plugin.get_event_handlers()

        self.assertIn(EventType.READY, handlers)

    def test__on_message_event_handler__callable_and_has_right_name(self):
        handlers = self.plugin.get_event_handlers()

        self.assertTrue(callable(handlers[EventType.READY]))
        self.assertEqual(
            handlers[EventType.READY].__name__, self.plugin._on_ready.__name__
        )
