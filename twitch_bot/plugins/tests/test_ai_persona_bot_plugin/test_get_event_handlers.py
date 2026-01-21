import unittest
from unittest.mock import AsyncMock

from twitch_bot.definitions import EventType
from twitch_bot.plugins.ai_persona_plugin import AIPersonaPlugin


class TestAIPersonaBotPluginGetEventHandlers(unittest.TestCase):

    def setUp(self) -> None:
        ai = AsyncMock()
        self.plugin: AIPersonaPlugin = AIPersonaPlugin(ai)

    def test__result__contains_message_event(self) -> None:
        event_handlers = self.plugin.get_event_handlers()

        self.assertIn(EventType.MESSAGE, event_handlers)

    def test__on_message_event_handler__callable_and_has_right_name(self) -> None:
        event_handlers = self.plugin.get_event_handlers()

        self.assertTrue(callable(event_handlers[EventType.MESSAGE]))
