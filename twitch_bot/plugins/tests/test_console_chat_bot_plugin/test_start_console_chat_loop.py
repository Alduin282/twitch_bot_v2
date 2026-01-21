from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch
from twitch_bot.plugins.console_chat_bot_plugin import ConsoleChatBotPlugin


class TestConsoleChatBotConsoleLoop(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.plugin = ConsoleChatBotPlugin()
        self.bot = MagicMock()

    async def test__no_channels__loop_not_started__logs_error(self) -> None:
        self.plugin._get_channels = MagicMock(return_value=[])

        with patch("twitch_bot.plugins.console_chat_bot_plugin.logger") as logger_mock:
            await self.plugin._start_console_chat_loop(self.bot)

        self.plugin._get_channels.assert_called_once_with(self.bot)
        logger_mock.error.assert_called_once()

    async def test__single_channel__sends_message_to_channel(self) -> None:
        channel = AsyncMock()
        self.plugin._get_channels = MagicMock(return_value=[channel])
        console_message = "console_message"

        with patch(
            "asyncio.to_thread", side_effect=[console_message, KeyboardInterrupt]
        ):
            with self.assertRaises(KeyboardInterrupt):
                await self.plugin._start_console_chat_loop(self.bot)

        channel.send.assert_awaited_once_with(console_message)

    async def test__multiply_channels__sends_message_to_all_channels(self) -> None:
        channel1 = AsyncMock()
        channel2 = AsyncMock()
        self.plugin._get_channels = MagicMock(return_value=[channel1, channel2])
        console_message = "console_message"

        with patch(
            "asyncio.to_thread", side_effect=[console_message, KeyboardInterrupt]
        ):
            with self.assertRaises(KeyboardInterrupt):
                await self.plugin._start_console_chat_loop(self.bot)

        channel1.send.assert_awaited_once_with(console_message)
        channel2.send.assert_awaited_once_with(console_message)
