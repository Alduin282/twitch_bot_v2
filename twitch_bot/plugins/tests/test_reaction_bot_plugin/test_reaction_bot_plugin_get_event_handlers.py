import unittest

from twitch_bot.definitions import EventType
from twitch_bot.plugins.reaction_bot_plugin import ReactionBotPlugin


class TestReactionBotPluginGetEventHandlers(unittest.TestCase):
    def setUp(self):
        self.plugin = ReactionBotPlugin(triggers=["trigger"], replies=["reply"])

    def test__result__contains_message_event(self) -> None:
        handlers = self.plugin.get_event_handlers()

        self.assertIn(EventType.MESSAGE, handlers)

    def test__on_message_event_handler__callable_and_has_right_name(self) -> None:
        handlers = self.plugin.get_event_handlers()

        self.assertTrue(callable(handlers[EventType.MESSAGE]))
        self.assertEqual(
            handlers[EventType.MESSAGE].__name__, self.plugin._on_message.__name__
        )
