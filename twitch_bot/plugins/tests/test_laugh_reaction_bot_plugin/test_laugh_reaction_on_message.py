import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from twitchio import Channel
from twitch_bot.plugins.laugh_reaction_bot_plugin import LaughReactionBotPlugin


class TestLaughReactionBotPluginOnMessageCooldown(unittest.IsolatedAsyncioTestCase):

    async def test__cooldown_not_ready__does_nothing(self) -> None:
        plugin = LaughReactionBotPlugin(cooldown_seconds=10)

        channel = self._get_channel_mock("test_channel")
        message = self._get_message_mock("test_message", channel)
        cooldown = self._get_cooldown_mock(is_ready=False)
        plugin._cooldowns[channel.name] = cooldown

        await plugin._on_message(MagicMock(), message)

        channel.send.assert_not_called()
        cooldown.trigger.assert_not_called()

    async def test__no_laugh_trigger__does_nothing(self) -> None:
        plugin = LaughReactionBotPlugin()

        channel = self._get_channel_mock("test_channel")
        message_without_laugh = self._get_message_mock(
            "message_without_laugh_trigger", channel
        )

        with patch(
            "twitch_bot.plugins.laugh_reaction_bot_plugin.asyncio.sleep",
            new_callable=AsyncMock,
        ):
            await plugin._on_message(MagicMock(), message_without_laugh)

        channel.send.assert_not_called()

    async def test__laugh_trigger__sends_reply_and_triggers_cooldown(self) -> None:
        plugin = LaughReactionBotPlugin()

        laugh_trigger = plugin.LAUGH_TRIGGERS[0]
        channel = self._get_channel_mock("test_channel")
        message_with_laugh_trigger = self._get_message_mock(laugh_trigger, channel)
        laugh_reply = plugin.LAUGH_REPLIES[0]

        with patch(
            "twitch_bot.plugins.laugh_reaction_bot_plugin.asyncio.sleep",
            new_callable=AsyncMock,
        ) as sleep_mock, patch(
            "twitch_bot.plugins.laugh_reaction_bot_plugin.random.choice",
            return_value=laugh_reply,
        ):
            await plugin._on_message(MagicMock(), message_with_laugh_trigger)

        sleep_mock.assert_awaited_once()
        channel.send.assert_awaited_once_with(laugh_reply)

        cooldown = plugin._cooldowns["test_channel"]
        self.assertFalse(cooldown.is_ready())

    async def test__second_message_within_cooldown__ignored(self) -> None:
        plugin = LaughReactionBotPlugin(cooldown_seconds=999)
        laugh_trigger = plugin.LAUGH_TRIGGERS[0]
        channel = self._get_channel_mock("test_channel")
        message = self._get_message_mock(laugh_trigger, channel)

        with patch(
            "twitch_bot.plugins.laugh_reaction_bot_plugin.asyncio.sleep",
            new_callable=AsyncMock,
        ), patch(
            "twitch_bot.plugins.laugh_reaction_bot_plugin.random.choice",
            return_value="LOL",
        ):
            await plugin._on_message(MagicMock(), message)
            await plugin._on_message(MagicMock(), message)

        channel.send.assert_awaited_once()

    @staticmethod
    def _get_channel_mock(channel_name: str) -> MagicMock:
        channel = AsyncMock()
        channel.name = channel_name
        return channel

    @staticmethod
    def _get_message_mock(content: str, channel: Channel) -> MagicMock:
        message = MagicMock()
        message.content = content
        message.channel = channel
        return message

    @staticmethod
    def _get_cooldown_mock(is_ready: bool) -> MagicMock:
        cooldown = MagicMock()
        cooldown.is_ready.return_value = is_ready
        return cooldown
