import unittest
from unittest.mock import AsyncMock

from twitch_bot.plugins.ai_question_spam_bot_plugin import AIQuestionSpamPlugin
from twitch_bot.definitions import EventType
from twitch_bot.plugins.helpers import DurationRange


class TestAIQuestionSpamBotPluginGetEventHandlers(unittest.TestCase):
    def setUp(self):
        ai = AsyncMock()
        self.plugin: AIQuestionSpamPlugin = AIQuestionSpamPlugin(
            ai, DurationRange(1.0, 2.0)
        )

    def test__result__contains_ready_event(self) -> None:
        handlers = self.plugin.get_event_handlers()

        self.assertIn(EventType.READY, handlers)

    def test__ready_event_handler__callable_and_has_right_name(self) -> None:
        handlers = self.plugin.get_event_handlers()

        self.assertTrue(callable(handlers[EventType.READY]))
