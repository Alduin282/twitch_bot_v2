import unittest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

from twitch_bot.plugins.tests.test_log_laugh_burst_bot_plugin.test_log_laugh_burst_base import (  # noqa: E501
    LogLaughBurstBotPluginTestBase,
)


class TestLogLaughBurstBotPluginOnMessage(
    unittest.IsolatedAsyncioTestCase, LogLaughBurstBotPluginTestBase
):

    async def test__laugh_burst_detected__log_called(self) -> None:
        plugin = self.create_reaction_rule(
            laugh_markers=("laugh_marker",),
            window_size_messages=3,
            required_matches=2,
        )

        message = self._get_message_mock("laugh_marker", "test_channel")
        bot = MagicMock()

        with patch.object(plugin, "_log_laugh", new_callable=AsyncMock) as log_mock:
            await plugin._on_message(bot, message)
            await plugin._on_message(bot, message)

            log_mock.assert_awaited_once()

    async def test__not_laugh_burst_detected__does_not_log(self) -> None:
        plugin = self.create_reaction_rule(
            laugh_markers=("laugh_marker",),
            window_size_messages=3,
            required_matches=2,
        )

        message = self._get_message_mock(
            content="content_without_laugh",
            channel="test_channel",
        )

        bot = MagicMock()

        with patch.object(plugin, "_log_laugh", new_callable=AsyncMock) as log_mock:
            await plugin._on_message(bot, message)
            await plugin._on_message(bot, message)
            await plugin._on_message(bot, message)

            log_mock.assert_not_awaited()

    async def test__cooldown_not_ready__does_not_log(self) -> None:
        plugin = self.create_reaction_rule(
            laugh_markers=("laugh_marker",),
            window_size_messages=3,
            required_matches=2,
            cooldown_seconds=9999,
        )

        message = self._get_message_mock("laugh_marker", "test_channel")
        bot = MagicMock()

        with patch.object(plugin, "_log_laugh", new_callable=AsyncMock) as log_mock:
            await plugin._on_message(bot, message)
            await plugin._on_message(bot, message)
            await plugin._on_message(bot, message)
            await plugin._on_message(bot, message)

            log_mock.assert_awaited_once()

    async def test__laughs_outside_window__does_not_log(self) -> None:
        plugin = self.create_reaction_rule(
            laugh_markers=("laugh_marker",),
            window_size_messages=3,
            required_matches=2,
        )

        bot = MagicMock()
        channel = "test_channel"

        message_laugh = self._get_message_mock("laugh_marker", channel)
        message_normal = self._get_message_mock("not_laugh", channel)

        with patch.object(plugin, "_log_laugh", new_callable=AsyncMock) as log_mock:
            await plugin._on_message(bot, message_laugh)
            await plugin._on_message(bot, message_normal)
            await plugin._on_message(bot, message_normal)
            await plugin._on_message(bot, message_laugh)

            log_mock.assert_not_awaited()

    @staticmethod
    def _get_message_mock(content: str, channel: str) -> MagicMock:
        message = MagicMock()
        message.content = content
        message.timestamp = datetime.now()
        message.channel.name = channel
        return message
