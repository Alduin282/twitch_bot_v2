import asyncio
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch
from twitchio import Channel
from twitch_bot.plugins.ai_question_spam_bot_plugin import AIQuestionSpamPlugin
from twitch_bot.plugins.helpers import DurationRange


class TestAIQuestionSpamOnReady(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.default_question = "test_question"
        self.ai_service = self._get_ai_service_mock(self.default_question)
        self.plugin = self._create_ai_question_plugin(self.ai_service)

    async def test__no_channels__logs_and_returns(self) -> None:
        bot = self._get_bot_mock(connected_channels=[])

        with self.assertLogs(
            "twitch_bot.plugins.ai_question_spam_bot_plugin",
            level="WARNING",
        ):
            await self.plugin._on_ready(bot)

    async def test__single_channel__sends_question(self) -> None:
        channel = self._get_channel_mock("test_channel")
        bot = self._get_bot_mock(connected_channels=[channel])

        with patch(
            "twitch_bot.plugins.ai_question_spam_bot_plugin.sleep_in_range",
            new_callable=AsyncMock,
            side_effect=[None, asyncio.CancelledError],
        ) as sleep_mock:
            sleep_mock.side_effect = [
                None,  # 1-я итерация
                asyncio.CancelledError,  # стоп
            ]

            with self.assertRaises(asyncio.CancelledError):
                await self.plugin._on_ready(bot)

        channel.send.assert_awaited_once_with(self.default_question)
        self.ai_service.ask_streamer.assert_awaited_once()

    async def test__multiple_channels__sends_questions_to_all_channels(self) -> None:
        channel1 = self._get_channel_mock("test_channel1")
        channel2 = self._get_channel_mock("test_channel2")
        bot = self._get_bot_mock(connected_channels=[channel1, channel2])

        with patch(
            "twitch_bot.plugins.ai_question_spam_bot_plugin.sleep_in_range",
            new_callable=AsyncMock,
            side_effect=[None, asyncio.CancelledError],
        ) as sleep_mock:
            sleep_mock.side_effect = [
                None,  # 1-я итерация
                asyncio.CancelledError,  # стоп
            ]

            with self.assertRaises(asyncio.CancelledError):
                await self.plugin._on_ready(bot)

        channel1.send.assert_awaited_once_with(self.default_question)
        channel2.send.assert_awaited_once_with(self.default_question)

    async def test__long_ai_question__is_trimmed_to_500_chars(self) -> None:
        long_question = "1" * 501
        ai_service = self._get_ai_service_mock(long_question)
        plugin = self._create_ai_question_plugin(ai_service)
        channel = self._get_channel_mock("test_channel")
        bot = self._get_bot_mock(connected_channels=[channel])

        with patch(
            "twitch_bot.plugins.ai_question_spam_bot_plugin.sleep_in_range",
            new_callable=AsyncMock,
            side_effect=[None, asyncio.CancelledError],
        ) as sleep_mock:
            sleep_mock.side_effect = [
                None,  # 1-я итерация
                asyncio.CancelledError,  # стоп
            ]

            with self.assertRaises(asyncio.CancelledError):
                await plugin._on_ready(bot)

        channel.send.assert_awaited_once_with(long_question[:500])
        ai_service.ask_streamer.assert_awaited_once()

    async def test__delay_start_seconds__sleep_called(self) -> None:
        delay = 5
        ai_service = self._get_ai_service_mock(self.default_question)
        plugin = self._create_ai_question_plugin(
            ai_service=ai_service, delay_seconds=delay
        )
        bot = self._get_bot_mock(connected_channels=[])

        with patch(
            "twitch_bot.plugins.ai_question_spam_bot_plugin.asyncio.sleep",
            new_callable=AsyncMock,
        ) as sleep_mock:
            await plugin._on_ready(bot)

        sleep_mock.assert_awaited_once_with(delay)

    def _create_ai_question_plugin(
        self, ai_service: MagicMock, delay_seconds: float = 0
    ):
        return AIQuestionSpamPlugin(
            ai_service=ai_service,
            interval=DurationRange(1, 2),
            delay_start_seconds=delay_seconds,
        )

    @staticmethod
    def _get_ai_service_mock(question: str) -> MagicMock:
        ai_service = MagicMock()
        ai_service.ask_streamer = AsyncMock(return_value=question)
        return ai_service

    @staticmethod
    def _get_channel_mock(channel_name: str) -> MagicMock:
        channel = AsyncMock()
        channel.name = channel_name
        return channel

    @staticmethod
    def _get_bot_mock(
        connected_channels: list[Channel], stream_channels: list[str] = []
    ) -> MagicMock:
        bot = MagicMock()
        bot.connected_channels = connected_channels
        streams = [MagicMock(channel=channel) for channel in stream_channels]
        bot.fetch_streams = AsyncMock(return_value=streams)
        return bot
