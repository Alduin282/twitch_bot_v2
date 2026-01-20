from collections import deque
from unittest.mock import MagicMock

from twitch_bot.plugins.tests.test_log_laugh_burst_bot_plugin.test_log_laugh_burst_base import (  # noqa: E501
    LogLaughBurstBotPluginTestBase,
)


class TestLogLaughBurstBotPluginShouldLog(LogLaughBurstBotPluginTestBase):

    def setUp(self) -> None:
        self.laugh_marker = "laugh_marker"

        self.cooldown = MagicMock()
        self.cooldown.is_ready.return_value = True

    def test__all_conditions_met__return_true(self) -> None:
        self.plugin = self.create_reaction_rule(
            laugh_markers=(self.laugh_marker,),
            required_matches=2,
        )
        window_messages_state = deque([self.laugh_marker, self.laugh_marker], maxlen=5)

        result = self.plugin._should_log(window_messages_state, self.cooldown)

        self.assertTrue(result)

    def test__not_laugh_message__return_false(self) -> None:
        self.plugin = self.create_reaction_rule(
            laugh_markers=(self.laugh_marker,),
            required_matches=2,
        )
        window_messages_state = deque(
            ["not_laugh_message", self.laugh_marker], maxlen=5
        )

        result = self.plugin._should_log(window_messages_state, self.cooldown)

        self.assertFalse(result)

    def test__cooldown_not_ready__false(self) -> None:
        self.plugin = self.create_reaction_rule(
            laugh_markers=(self.laugh_marker,),
            required_matches=2,
        )
        self.cooldown.is_ready.return_value = False
        window_messages_state = deque([self.laugh_marker, self.laugh_marker], maxlen=5)

        result = self.plugin._should_log(window_messages_state, self.cooldown)

        self.assertFalse(result)
