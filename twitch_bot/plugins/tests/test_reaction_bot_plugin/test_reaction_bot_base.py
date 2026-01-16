import unittest

from twitch_bot.plugins.reaction_bot_plugin import ReactionBotPlugin


class ReactionPluginTestBase(unittest.TestCase):
    def create_reaction_plugin(
        self,
        triggers: tuple[str, ...] = ("trigger",),
        replies: tuple[str, ...] = ("reply",),
        reaction_probability: float = 1.0,
        ignore_echo: bool = True,
        cooldown_seconds: float = 2.0,
        pre_reaction_delay_max: float = 0.4,
        pre_reaction_delay_min: float = 0.3,
    ) -> ReactionBotPlugin:
        return ReactionBotPlugin(
            triggers=triggers,
            replies=replies,
            reaction_probability=reaction_probability,
            ignore_echo=ignore_echo,
            cooldown_seconds=cooldown_seconds,
            pre_reaction_delay_max=pre_reaction_delay_max,
            pre_reaction_delay_min=pre_reaction_delay_min,
        )
