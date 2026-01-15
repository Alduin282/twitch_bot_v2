import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock

from twitch_bot.plugins.log_start_bot_plugin import LogStartBotPlugin


class TestLogStartBotPluginOnReady(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.plugin = LogStartBotPlugin()
        self.bot = MagicMock()

    async def test__logs__bot_nick_in_logs(self):
        self.bot.nick = "TestBot"

        with self.assertLogs(
            "twitch_bot.plugins.log_start_bot_plugin", level="INFO"
        ) as cm:
            await self.plugin._on_ready(self.bot)

        logs = cm.output
        self.assertTrue(any("Logged in as TestBot" in message for message in logs))

    async def test__logs__connected_channels_in_logs(self):
        self.channel_1 = SimpleNamespace(name="channel_one")
        self.channel_2 = SimpleNamespace(name="channel_two")
        self.bot.connected_channels = [self.channel_1, self.channel_2]

        with self.assertLogs(
            "twitch_bot.plugins.log_start_bot_plugin", level="INFO"
        ) as log_context:
            await self.plugin._on_ready(self.bot)

        logs = log_context.output
        self.assertTrue(any("channel_one" in message for message in logs))
        self.assertTrue(any("channel_two" in message for message in logs))
