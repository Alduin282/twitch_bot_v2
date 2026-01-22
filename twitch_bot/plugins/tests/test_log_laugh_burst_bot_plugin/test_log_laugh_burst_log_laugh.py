from datetime import datetime, timezone
import os
import tempfile
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from twitch_bot.plugins.log_laugh_burst_bot_plugin import LogLaughBurstBotPlugin


class TestLogLaughBurstBotPluginLogLaughNoStream(unittest.IsolatedAsyncioTestCase):

    async def test__successful_log__writes_expected_log_line(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = os.path.join(temp_dir, "laugh.log")

            plugin = LogLaughBurstBotPlugin(log_file_path=log_path)

            message_time = datetime(2024, 1, 1, 12, 0, 0)
            stream_start_time = datetime(2024, 1, 1, 11, 0, 0, tzinfo=timezone.utc)
            channel_name = "test_channel"

            with patch.object(
                plugin,
                "_get_start_stream_time",
                new_callable=AsyncMock,
                return_value=stream_start_time,
            ):
                await plugin._log_laugh(
                    channel_name=channel_name,
                    message_timestamp=message_time,
                    bot=MagicMock(),
                )

            with open(log_path, encoding="utf-8") as f:
                content = f.read()

            self.assertIn(f"{channel_name} {plugin.LAUGH_BURST_LOG_PREFIX}", content)
            self.assertIn(str(message_time), content)

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
        ) as write_log_in_file_mock, patch(
            "twitch_bot.plugins.log_laugh_burst_bot_plugin.logger.warning"
        ) as warning_mock:
            await plugin._log_laugh(
                "channel",
                datetime.now(),
                MagicMock(),
            )

            write_log_in_file_mock.assert_not_called()
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
