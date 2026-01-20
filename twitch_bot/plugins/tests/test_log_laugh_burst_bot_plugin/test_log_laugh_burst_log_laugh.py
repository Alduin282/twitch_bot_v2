from datetime import datetime, timezone
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from twitch_bot.plugins.log_laugh_burst_bot_plugin import LogLaughBurstBotPlugin


class TestLogLaughBurstBotPluginLogLaughNoStream(unittest.IsolatedAsyncioTestCase):
    # пиздец
    async def test__successful_log__writes_expected_log_line(self) -> None:
        plugin = LogLaughBurstBotPlugin()

        message_ts = datetime(2024, 1, 1, 12, 0, 0)
        stream_start = datetime(2024, 1, 1, 11, 0, 0, tzinfo=timezone.utc)
        stream_time = message_ts.replace(tzinfo=timezone.utc) - stream_start

        with patch.object(
            plugin,
            "_get_start_stream_time",
            new_callable=AsyncMock,
            return_value=stream_start,
        ), patch.object(
            plugin,
            "_write_log_line",
            new_callable=AsyncMock,
        ) as write_mock:
            await plugin._log_laugh(
                channel_name="channel",
                message_timestamp=message_ts,
                bot=MagicMock(),
            )

            write_mock.assert_awaited_once()
            self.assertEqual(len(write_mock.await_args_list), 1)

            call = write_mock.await_args_list[0]
            log_line: str = call.args[0]

            self.assertIn("channel LAUGH-BURST", log_line)
            self.assertIn(str(message_ts), log_line)
            self.assertIn(str(stream_time), log_line)

    async def test__no_stream__logs_warning_and_returns(self) -> None:
        plugin = LogLaughBurstBotPlugin()

        with patch.object(
            plugin,
            "_get_start_stream_time",
            new_callable=AsyncMock,
            return_value=None,
        ), patch.object(
            plugin,
            "_write_log_line",
            new_callable=AsyncMock,
        ) as write_mock, patch(
            "twitch_bot.plugins.log_laugh_burst_bot_plugin.logger.warning"
        ) as warning_mock:
            await plugin._log_laugh(
                "channel",
                datetime.now(),
                MagicMock(),
            )

            write_mock.assert_not_called()
            warning_mock.assert_called_once()

    async def test__write_error__logs_error(self) -> None:
        plugin = LogLaughBurstBotPlugin()

        with patch.object(
            plugin,
            "_get_start_stream_time",
            new_callable=AsyncMock,
            return_value=datetime(2024, 1, 1, tzinfo=timezone.utc),
        ), patch.object(
            plugin,
            "_write_log_line",
            new_callable=AsyncMock,
            side_effect=RuntimeError("disk error"),
        ), patch(
            "twitch_bot.plugins.log_laugh_burst_bot_plugin.logger.error"
        ) as error_mock:
            await plugin._log_laugh(
                "channel",
                datetime.now(),
                MagicMock(),
            )

            error_mock.assert_called_once()
