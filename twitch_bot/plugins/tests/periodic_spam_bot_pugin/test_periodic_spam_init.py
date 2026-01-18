import unittest

from twitch_bot.plugins.periodic_spam_bot_plugin import PeriodicSpamBotPlugin
from twitch_bot.plugins.helpers import DurationRange


class TestPeriodicSpamBotPluginInit(unittest.TestCase):

    def test__messages_empty__value_error(self):
        empty_messages = []

        with self.assertRaises(ValueError):
            PeriodicSpamBotPlugin(
                messages=empty_messages,
                interval=DurationRange(1.0, 2.0),
            )

    def test__delay_below_zero__value_error(self):
        below_zero_delay = -1

        with self.assertRaises(ValueError):
            PeriodicSpamBotPlugin(
                messages=["hello"],
                interval=DurationRange(1.0, 2.0),
                delay_start_seconds=below_zero_delay,
            )
