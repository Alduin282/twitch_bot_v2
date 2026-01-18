import unittest
from collections import deque

from twitch_bot.plugins.log_laugh_burst_bot_plugin import LogLaughBurstBotPlugin


class LogLaughBurstBotPluginTestBase(unittest.TestCase):
    def create_reaction_rule(
        self,
        laugh_markers=("laugh_marker",),
        window_size_messages=10,
        required_matches=5,
        cooldown_seconds=15,
        log_file_path="log.txt",
    ) -> LogLaughBurstBotPlugin:
        return LogLaughBurstBotPlugin(
            laugh_markers=laugh_markers,
            window_size_messages=window_size_messages,
            required_matches=required_matches,
            cooldown_seconds=cooldown_seconds,
            log_file_path=log_file_path,
        )


class TestLogLaughBurstBotPluginHasLaughBurst(LogLaughBurstBotPluginTestBase):

    def test__enough_laugh_messages__true(self) -> None:
        messages = deque(
            ["lol", "hello", "lol", "lol", "test"],
            maxlen=5,
        )

        self.assertTrue(plugin._has_laugh_burst(messages))

    def test__not_enough_laugh_messages__false(self) -> None:
        messages = deque(
            ["lol", "hello", "test", "world"],
            maxlen=5,
        )

        self.assertFalse(self.plugin._has_laugh_burst(messages))
