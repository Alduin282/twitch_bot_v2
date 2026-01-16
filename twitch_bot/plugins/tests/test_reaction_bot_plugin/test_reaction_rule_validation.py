import unittest
import uuid
from twitch_bot.plugins.helpers import DurationRange
from twitch_bot.plugins.reaction_bot_plugin import ReactionRule


class ReactionRuleTestBase(unittest.TestCase):
    def create_reaction_rule(
        self,
        triggers: tuple[str, ...] = ("trigger",),
        replies: tuple[str, ...] = ("reply",),
        reaction_probability: float = 0.1,
        ignore_echo: bool = True,
        cooldown_seconds: float = 2.0,
        pre_reaction_delay: DurationRange = DurationRange(0.3, 0.4),
    ) -> ReactionRule:
        return ReactionRule(
            triggers=triggers,
            replies=replies,
            reaction_probability=reaction_probability,
            ignore_echo=ignore_echo,
            cooldown_seconds=cooldown_seconds,
            pre_reaction_delay=pre_reaction_delay,
        )


class TestReactionRuleValidation(ReactionRuleTestBase):
    def test__valid_rule__no_errors(self):
        valid_reaction_rule = self.create_reaction_rule()

        self.assertIsInstance(valid_reaction_rule, ReactionRule)

    def test__probability_less_than_zero__value_error(self):
        with self.assertRaises(ValueError):
            self.create_reaction_rule(reaction_probability=-0.1)

    def test__probability_greater_than_one__value_error(self):
        with self.assertRaises(ValueError):
            self.create_reaction_rule(reaction_probability=1.1)

    def test__probability_zero__no_errors(self):
        rule = self.create_reaction_rule(reaction_probability=0.0)
        self.assertEqual(rule.reaction_probability, 0.0)

    def test__probability_one__no_errors(self):
        rule = self.create_reaction_rule(reaction_probability=1.0)
        self.assertEqual(rule.reaction_probability, 1.0)

    def test__negative_cooldown__value_error(self):
        with self.assertRaises(ValueError):
            self.create_reaction_rule(cooldown_seconds=-1.0)

    def test__zero_cooldown__no_errors(self):
        rule = self.create_reaction_rule(cooldown_seconds=0.0)
        self.assertEqual(rule.cooldown_seconds, 0.0)

    def test__empty_triggers__value_error(self):
        empty_triggers = ()
        with self.assertRaises(ValueError):
            self.create_reaction_rule(triggers=empty_triggers)

    def test__empty_replies__value_error(self):
        empty_replies = ()
        with self.assertRaises(ValueError):
            self.create_reaction_rule(replies=empty_replies)

    def test__crate_reaction_rule__valid_uuid4(self):
        rule = self.create_reaction_rule()

        parsed = uuid.UUID(rule._uid, version=4)

        self.assertEqual(parsed.version, 4)
        self.assertEqual(str(parsed), rule._uid)

    def test__trigger_with_multiple_words__value_error(self):
        trigger_with_multiple_words = ("trigger with spaces",)

        with self.assertRaises(ValueError):
            self.create_reaction_rule(triggers=trigger_with_multiple_words)
