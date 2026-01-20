from collections import deque

from twitch_bot.plugins.tests.test_log_laugh_burst_bot_plugin.test_log_laugh_burst_base import (  # noqa: E501
    LogLaughBurstBotPluginTestBase,
)


class TestLogLaughBurstBotPluginHasLaughBurst(LogLaughBurstBotPluginTestBase):

    def test__enough_laugh_messages__return_true(self) -> None:
        laugh_markers = ("laugh_marker",)
        plugin = self.create_reaction_rule(
            laugh_markers=laugh_markers, window_size_messages=3, required_matches=2
        )
        messages = deque(
            ["laugh_marker_and_something", "not_marker", "laugh_marker"],
            maxlen=plugin.laugh_rule.window_size_messages,
        )

        result = plugin._has_laugh_burst(messages)

        self.assertTrue(result)

    def test__not_enough_laugh_messages__return_false(self) -> None:
        laugh_markers = ("laugh_marker",)
        plugin = self.create_reaction_rule(
            laugh_markers=laugh_markers, window_size_messages=3, required_matches=2
        )
        messages = deque(
            ["not_marker", "not_marker", "laugh_marker"],
            maxlen=plugin.laugh_rule.window_size_messages,
        )

        result = plugin._has_laugh_burst(messages)

        self.assertFalse(result)
