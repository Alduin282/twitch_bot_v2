from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock

from twitch_bot.plugins.ai_question_spam_bot_plugin import AIQuestionSpamPlugin
from twitch_bot.plugins.helpers import DurationRange


class TestAIQuestionSpamGetStream(IsolatedAsyncioTestCase):

    async def test__stream_found__returns_stream(self) -> None:
        plugin = AIQuestionSpamPlugin(
            ai_service=MagicMock(),
            interval=DurationRange(1, 2),
        )

        stream = MagicMock()
        bot = MagicMock()
        bot.fetch_streams = AsyncMock(return_value=[stream])

        result = await plugin._get_stream(bot, "channel")

        self.assertIs(result, stream)

    async def test__no_streams__returns_none(self) -> None:
        plugin = AIQuestionSpamPlugin(
            ai_service=MagicMock(),
            interval=DurationRange(1, 2),
        )

        bot = MagicMock()
        bot.fetch_streams = AsyncMock(return_value=[])

        result = await plugin._get_stream(bot, "channel")

        self.assertIsNone(result)
