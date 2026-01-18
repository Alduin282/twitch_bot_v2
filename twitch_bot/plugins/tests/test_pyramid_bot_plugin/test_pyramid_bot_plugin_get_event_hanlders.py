import unittest

from twitch_bot.definitions import EventType
from twitch_bot.plugins.pyramid_bot_plugin import PyramidBotPlugin


class TestPyramidBotPluginGetEventHandlers(unittest.TestCase):

    def setUp(self) -> None:
        self.plugin: PyramidBotPlugin = PyramidBotPlugin()

    def test__result__contains_message_event(self) -> None:
        event_handlers = self.plugin.get_event_handlers()

        self.assertIn(EventType.MESSAGE, event_handlers)

    def test__on_message_event_handler__callable_and_has_right_name(self) -> None:
        event_handlers = self.plugin.get_event_handlers()

        self.assertTrue(callable(event_handlers[EventType.MESSAGE]))
        self.assertEqual(
            event_handlers[EventType.MESSAGE].__name__, self.plugin._on_message.__name__
        )
