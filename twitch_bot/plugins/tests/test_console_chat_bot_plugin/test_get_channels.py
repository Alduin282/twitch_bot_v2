from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch
from twitch_bot.plugins.console_chat_bot_plugin import ConsoleChatBotPlugin


class TestConsoleChatBotGetChannels(IsolatedAsyncioTestCase):

    async def test__no_target_channels__returns_connected_channels(self) -> None:
        plugin = ConsoleChatBotPlugin()
        bot = MagicMock()

        channel1 = MagicMock()
        channel2 = MagicMock()
        bot.connected_channels = [channel1, channel2]

        result = plugin._get_channels(bot)

        self.assertEqual(result, [channel1, channel2])

    async def test__target_channels_all_exist__return_target_channels(self) -> None:
        channel_name_1 = "channel_name_1"
        channel_name_2 = "channel_name_2"
        plugin = ConsoleChatBotPlugin(target_channels=[channel_name_1, channel_name_2])

        channel1 = self._get_channel_mock(channel_name_1)
        channel2 = self._get_channel_mock(channel_name_2)
        bot = MagicMock()
        bot.get_channel.side_effect = [channel1, channel2]

        result = plugin._get_channels(bot)

        self.assertEqual(result, [channel1, channel2])
        bot.get_channel.assert_any_call(channel_name_1)
        bot.get_channel.assert_any_call(channel_name_2)

    async def test__target_channels_some_missing__return_channels_without_missing(
        self,
    ) -> None:
        target_channel = "target channel"
        plugin = ConsoleChatBotPlugin(target_channels=[target_channel, "missing"])
        bot = MagicMock()

        channel1 = self._get_channel_mock(target_channel)
        bot.get_channel.side_effect = [channel1, None]

        with patch("twitch_bot.plugins.console_chat_bot_plugin.logger") as logger_mock:
            result = plugin._get_channels(bot)

        self.assertEqual(result, [channel1])
        logger_mock.warning.assert_called_once()

    async def test__target_channels_all_missing__returns_empty(self) -> None:
        plugin = ConsoleChatBotPlugin(target_channels=["missing1", "missing2"])
        bot = MagicMock()

        bot.get_channel.return_value = None

        with patch("twitch_bot.plugins.console_chat_bot_plugin.logger") as logger_mock:
            result = plugin._get_channels(bot)

        self.assertEqual(result, [])
        self.assertEqual(logger_mock.warning.call_count, 2)

    def _get_channel_mock(self, name: str) -> MagicMock:
        channel = MagicMock()
        channel.name = name
        return channel
