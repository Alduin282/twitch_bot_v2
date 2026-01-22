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
        plugin = self.create_reaction_plugin(cooldown_seconds=9999)

        await plugin._on_message(self.bot, self.message)
        await plugin._on_message(self.bot, self.message)

        mock_react_with_delay.assert_called_once()

    @patch.object(ReactionBotPlugin, "_react_with_delay", new_callable=AsyncMock)
    async def test__cooldown_ready__reacts(
        self, mock_react_with_delay: AsyncMock
    ) -> None:
        plugin = self.create_reaction_plugin(cooldown_seconds=0)

        bot = MagicMock()

        await plugin._on_message(bot, self.message)
        await plugin._on_message(bot, self.message)

        self.assertEqual(mock_react_with_delay.await_count, 2)

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
