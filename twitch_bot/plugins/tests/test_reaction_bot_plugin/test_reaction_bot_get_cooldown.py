from twitch_bot.plugins.helpers import Cooldown
from twitch_bot.plugins.tests.test_reaction_bot_plugin.test_reaction_bot_base import (
    ReactionPluginTestBase,
)


class TestReactionBotPluginCooldown(ReactionPluginTestBase):
    default_cooldown_seconds = 10

    def test__fist_time_channel_event__cooldown_created(self):
        new_channel_name = "new_channel"
        plugin = self.create_reaction_plugin(
            cooldown_seconds=self.default_cooldown_seconds
        )

        cooldown = plugin._get_channel_cooldown(new_channel_name)

        self.assertIsInstance(cooldown, Cooldown)
        self.assertEqual(cooldown._duration, self.default_cooldown_seconds)

    def test__second_time_get_channel_cooldown__return_existing(self):
        channel_name = "channel"
        plugin = self.create_reaction_plugin(
            cooldown_seconds=self.default_cooldown_seconds
        )

        cooldown1 = plugin._get_channel_cooldown(channel_name)
        cooldown2 = plugin._get_channel_cooldown(channel_name)

        self.assertIs(cooldown1, cooldown2)
