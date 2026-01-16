import unittest

from twitch_bot.plugins.helpers import DurationRange
from twitch_bot.plugins.reaction_bot_plugin import ReactionBotPlugin, ReactionRule


class TestReactionBotPluginInit(unittest.TestCase):

    def test__plugin_initializes__initialized_correctly(self):
        test_replies = ("test_reply",)
        test_triggers = ("test_trigger",)
        test_cooldown = 1
        test_delay_max = 0.3
        test_delay_min = 0.2
        test_probability = 1.0
        test_ignore_echo = True

        plugin = ReactionBotPlugin(
            replies=test_replies,
            triggers=test_triggers,
            cooldown_seconds=test_cooldown,
            ignore_echo=test_ignore_echo,
            pre_reaction_delay_max=test_delay_max,
            pre_reaction_delay_min=test_delay_min,
            reaction_probability=test_probability,
        )
        rule = plugin.reaction_rule

        self.assertIsInstance(rule, ReactionRule)

        self.assertEqual(rule.triggers, test_triggers)
        self.assertEqual(rule.replies, test_replies)
        self.assertEqual(rule.cooldown_seconds, test_cooldown)
        self.assertEqual(rule.ignore_echo, test_ignore_echo)
        self.assertEqual(rule.reaction_probability, test_probability)

        self.assertEqual(
            rule.pre_reaction_delay,
            DurationRange(
                min_seconds=test_delay_min,
                max_seconds=test_delay_max,
            ),
        )

        self.assertIsInstance(plugin._cooldowns, dict)
        self.assertEqual(plugin._cooldowns, {})
