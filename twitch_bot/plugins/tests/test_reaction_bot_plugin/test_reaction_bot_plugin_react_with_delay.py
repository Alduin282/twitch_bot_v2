import unittest
from unittest.mock import AsyncMock, patch

from twitch_bot.plugins.helpers import DurationRange
from twitch_bot.plugins.reaction_bot_plugin import ReactionBotPlugin, ReactionRule


class TestReactionBotPluginReactWithDelay(unittest.IsolatedAsyncioTestCase):

    @patch("twitch_bot.plugins.reaction_bot_plugin.random.choice")
    @patch(
        "twitch_bot.plugins.reaction_bot_plugin.sleep_in_range", new_callable=AsyncMock
    )
    async def test__react_with_delay__sleeps_and_sends_reply(
        self, mock_sleep_in_range: AsyncMock, mock_random_choice: AsyncMock
    ):
        chosen_reply = "chosen_reply"
        replies = ("chosen_reply", "reply")
        mock_random_choice.return_value = chosen_reply

        reaction_rule = ReactionRule(
            triggers=("trigger",),
            replies=replies,
            reaction_probability=1.0,
            ignore_echo=True,
            cooldown_seconds=0,
            pre_reaction_delay=DurationRange(0.1, 0.2),
        )

        message = AsyncMock()
        message.channel.send = AsyncMock()

        await ReactionBotPlugin._react_with_delay(message, reaction_rule)

        mock_sleep_in_range.assert_awaited_once_with(reaction_rule.pre_reaction_delay)
        mock_random_choice.assert_called_once_with(replies)
        message.channel.send.assert_awaited_once_with(chosen_reply)
