import unittest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

from twitch_bot.plugins.tests.test_log_laugh_burst_bot_plugin.test_log_laugh_burst_base import (  # noqa: E501
    LogLaughBurstBotPluginTestBase,
)


class TestLogLaughBurstBotPluginOnMessage(
    unittest.IsolatedAsyncioTestCase, LogLaughBurstBotPluginTestBase
):

    async def test__laugh_burst_detected__log_called_and_cooldown_triggered(
        self,
    ) -> None:
        laugh_marker = "laugh_marker"
        plugin = self.create_reaction_rule(
            laugh_markers=(laugh_marker,),
            window_size_messages=3,
            required_matches=2,
        )

        message_with_laugh = self._get_message_mock(laugh_marker, "test_channel")

        bot = MagicMock()

        with patch.object(
            plugin, "_log_laugh", new_callable=AsyncMock
        ) as log_mock, patch.object(plugin, "_get_channel_cooldown") as cooldown_mock:
            cooldown = self._get_cooldown_mock(is_ready=True)
            cooldown_mock.return_value = cooldown

            # laugh burst
            await plugin._on_message(bot, message_with_laugh)
            await plugin._on_message(bot, message_with_laugh)

            log_mock.assert_awaited_once()
            cooldown.trigger.assert_called_once()

    async def test__not_laugh_burst_detected__does_not_log(
        self,
    ) -> None:
        plugin = self.create_reaction_rule(
            laugh_markers=("laugh_marker",),
            window_size_messages=3,
            required_matches=2,
        )

        message_without_laugh = self._get_message_mock(
            content="content_without_laugh", channel="test_channel"
        )

        bot = MagicMock()

        with patch.object(
            plugin, "_log_laugh", new_callable=AsyncMock
        ) as log_mock, patch.object(plugin, "_get_channel_cooldown") as cooldown_mock:
            cooldown = self._get_cooldown_mock(is_ready=True)
            cooldown_mock.return_value = cooldown

            # 3 messages, no burst
            await plugin._on_message(bot, message_without_laugh)
            await plugin._on_message(bot, message_without_laugh)
            await plugin._on_message(bot, message_without_laugh)

            log_mock.assert_not_awaited()
            cooldown.trigger.assert_not_called()

    async def test__cooldown_not_ready__does_not_log(self) -> None:
        laugh_marker = "laugh_marker"
        plugin = self.create_reaction_rule(
            laugh_markers=(laugh_marker,),
            window_size_messages=3,
            required_matches=2,
        )

        message_with_laugh = self._get_message_mock(laugh_marker, "test_channel")

        bot = MagicMock()

        with patch.object(
            plugin, "_log_laugh", new_callable=AsyncMock
        ) as log_mock, patch.object(plugin, "_get_channel_cooldown") as cooldown_mock:
            cooldown = self._get_cooldown_mock(is_ready=False)
            cooldown_mock.return_value = cooldown

            # laugh burst
            await plugin._on_message(bot, message_with_laugh)
            await plugin._on_message(bot, message_with_laugh)

            log_mock.assert_not_awaited()
            cooldown.trigger.assert_not_called()

    async def test__laughs_outside_window__does_not_log(self) -> None:
        laugh_marker = "laugh_marker"
        plugin = self.create_reaction_rule(
            laugh_markers=(laugh_marker,),
            window_size_messages=3,
            required_matches=2,
        )

        bot = MagicMock()

        channel = "test_channel"
        message_laugh = self._get_message_mock(laugh_marker, channel)
        message_normal = self._get_message_mock("not_marker_of_laugh", channel)

        with patch.object(
            plugin, "_log_laugh", new_callable=AsyncMock
        ) as log_mock, patch.object(plugin, "_get_channel_cooldown") as cooldown_mock:
            cooldown = self._get_cooldown_mock(is_ready=True)
            cooldown_mock.return_value = cooldown

            # 2 сообщения смеха, но оттделены друг от друга
            await plugin._on_message(bot, message_laugh)
            await plugin._on_message(bot, message_normal)
            await plugin._on_message(bot, message_normal)
            await plugin._on_message(bot, message_laugh)

            log_mock.assert_not_awaited()
            cooldown.trigger.assert_not_called()

    @staticmethod
    def _get_message_mock(content: str, channel: str) -> MagicMock:
        message = MagicMock()
        message.content = content
        message.timestamp = datetime.now()
        message.channel.name = channel
        return message

    @staticmethod
    def _get_cooldown_mock(is_ready: bool) -> MagicMock:
        cooldown = MagicMock()
        cooldown.is_ready.return_value = is_ready
        return cooldown
