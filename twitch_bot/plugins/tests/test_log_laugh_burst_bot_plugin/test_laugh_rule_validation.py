import unittest

from twitch_bot.plugins.log_laugh_burst_bot_plugin import LaughRule


class LaughRuleTestBase(unittest.TestCase):
    def create_reaction_rule(
        self,
        laugh_markers=("laugh_marker",),
        window_size_messages=10,
        required_matches=5,
        cooldown_seconds=15,
        log_file_path="log.txt",
    ) -> LaughRule:
        return LaughRule(
            laugh_markers=laugh_markers,
            window_size_messages=window_size_messages,
            required_matches=required_matches,
            cooldown_seconds=cooldown_seconds,
            log_file_path=log_file_path,
        )


class TestLaughRuleValidation(LaughRuleTestBase):

    def test__valid_rule__no_errors(self) -> None:
        laugh_rule = self.create_reaction_rule(
            laugh_markers=("laugh_marker",),
            window_size_messages=10,
            required_matches=5,
            cooldown_seconds=10,
            log_file_path="log.txt",
        )

        self.assertIsInstance(laugh_rule, LaughRule)

    def test__empty_laugh_markers__value_error(self) -> None:
        with self.assertRaises(ValueError):
            empty_laugh_markers = []
            self.create_reaction_rule(laugh_markers=empty_laugh_markers)

    def test__window_size_equal_zero__value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.create_reaction_rule(window_size_messages=0)

    def test__required_matches_equal_zero__value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.create_reaction_rule(required_matches=0)

    def test__required_matches_more_than_window__value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.create_reaction_rule(window_size_messages=10, required_matches=11)

    def test__negative_cooldown__value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.create_reaction_rule(cooldown_seconds=-1)
