import unittest

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
