import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from twitch_bot.plugins.helpers import Cooldown
from twitch_bot.plugins.reaction_bot_plugin import ReactionBotPlugin
from twitch_bot.plugins.tests.test_reaction_bot_plugin.test_reaction_bot_base import (
    ReactionPluginTestBase,
)


class TestReactionBotPluginOnMessage(
    unittest.IsolatedAsyncioTestCase, ReactionPluginTestBase
):

    async def asyncSetUp(self) -> None:
        self.plugin = self.create_reaction_plugin()

        self.bot: MagicMock = MagicMock()

        self.message: MagicMock = MagicMock()
        self.message.content = "message with trigger"
        self.message.echo = False
        self.message.channel.name = "test_channel"

    @patch.object(ReactionBotPlugin, "_react_with_delay", new_callable=AsyncMock)
    async def test__cooldown_not_ready__no_reaction(
        self, mock_react_with_delay: AsyncMock
    ) -> None:
        cooldown: MagicMock = MagicMock(spec=Cooldown)
        cooldown.is_ready.return_value = False

        self.plugin._cooldowns[self.message.channel.name] = cooldown

        await self.plugin._on_message(self.bot, self.message)

        cooldown.is_ready.assert_called_once()
        mock_react_with_delay.assert_not_called()
        cooldown.trigger.assert_not_called()

    @patch.object(ReactionBotPlugin, "_react_with_delay", new_callable=AsyncMock)
    async def test__cooldown_ready__reacts_and_triggers_cooldown(
        self, mock_react_with_delay: AsyncMock
    ) -> None:
        cooldown: MagicMock = MagicMock(spec=Cooldown)
        cooldown.is_ready.return_value = True
        self.plugin._cooldowns[self.message.channel.name] = cooldown

        await self.plugin._on_message(self.bot, self.message)

        cooldown.is_ready.assert_called_once()
        mock_react_with_delay.assert_awaited_once_with(
            self.message, self.plugin.reaction_rule
        )
        cooldown.trigger.assert_called_once()

    @patch.object(ReactionBotPlugin, "_react_with_delay", new_callable=AsyncMock)
    async def test__first_reaction_event_by_channel__cooldown_created(
        self,
        mock_react_with_delay: AsyncMock,
    ) -> None:

        await self.plugin._on_message(self.bot, self.message)

        self.assertIn(self.message.channel.name, self.plugin._cooldowns)
        self.assertIsInstance(
            self.plugin._cooldowns[self.message.channel.name], Cooldown
        )
