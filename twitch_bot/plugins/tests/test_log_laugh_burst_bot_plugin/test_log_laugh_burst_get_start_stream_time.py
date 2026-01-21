import unittest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

from twitch_bot.plugins.log_laugh_burst_bot_plugin import LogLaughBurstBotPlugin


class TestLogLaughBurstBotPluginGetStartStreamTime(unittest.IsolatedAsyncioTestCase):

    async def test__active_stream__returns_start_time(self) -> None:
        plugin = LogLaughBurstBotPlugin()

        stream = MagicMock()
        stream.started_at = datetime.now()

        bot = MagicMock()
        bot.fetch_streams = AsyncMock(return_value=[stream])

        result = await plugin._get_start_stream_time(bot, "channel")

        self.assertEqual(result, stream.started_at)

    async def test__no_active_stream__returns_none(self) -> None:
        plugin = LogLaughBurstBotPlugin()

        bot = MagicMock()
        bot.fetch_streams = AsyncMock(return_value=[])

        result = await plugin._get_start_stream_time(bot, "channel")

        self.assertIsNone(result)
        with patch(
            "twitch_bot.plugins.log_laugh_burst_bot_plugin.logger.warning"
        ) as warning_mock:
            result = await plugin._get_start_stream_time(bot, "channel")

            self.assertIsNone(result)
            warning_mock.assert_called_once()
