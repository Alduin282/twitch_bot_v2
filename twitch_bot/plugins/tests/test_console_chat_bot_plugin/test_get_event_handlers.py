import unittest

from twitch_bot.plugins.console_chat_bot_plugin import ConsoleChatBotPlugin
from twitch_bot.definitions import EventType


class TestConsoleChatBotPluginGetEventHandlers(unittest.TestCase):

    def setUp(self):
        self.plugin = ConsoleChatBotPlugin()

    def test__result__contains_message_event(self):
        handlers = self.plugin.get_event_handlers()

        self.assertIn(EventType.READY, handlers)

    def test__on_message_event_handler__callable_and_has_right_name(self):
        handlers = self.plugin.get_event_handlers()

        self.assertTrue(callable(handlers[EventType.READY]))
