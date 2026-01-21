from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock

from twitch_bot.twitch_bot import TwitchBot
from twitch_bot.definitions import EventType


class TestTwitchBotEventReady(IsolatedAsyncioTestCase):

    async def test__event_ready__dispatches_ready_event(self) -> None:
        dispatcher = AsyncMock()

        bot = TwitchBot(
            token="test_token",
            channels_to_connect=["channels_to_connect"],
            twitch_secret_key="twitch_secret_key",
            event_dispatcher=dispatcher,
        )

        await bot.event_ready()

        dispatcher.dispatch.assert_awaited_once_with(
            EventType.READY,
            bot,
        )

    async def test__event_message__dispatches_message_event(self) -> None:
        dispatcher = AsyncMock()

        bot = TwitchBot(
            token="test_token",
            channels_to_connect=["channels_to_connect"],
            twitch_secret_key="twitch_secret_key",
            event_dispatcher=dispatcher,
        )

        message = MagicMock()

        await bot.event_message(message)

        dispatcher.dispatch.assert_awaited_once_with(
            EventType.MESSAGE,
            bot,
            message,
        )
