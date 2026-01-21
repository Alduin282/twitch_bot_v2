from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock
from twitch_bot.event_dispatchers.event_dispatcher import EventDispatcher
from twitch_bot.plugins.bot_plugin import BotPlugin
from twitch_bot.twitch_bot import TwitchBot
from twitch_bot.definitions import EventType


class TestPlugin(BotPlugin):
    def __init__(self):
        self.ready_called = False
        self.message_called_with = []

    def get_event_handlers(self):
        return {
            EventType.READY: self.on_ready,
            EventType.MESSAGE: self.on_message,
        }

    async def on_ready(self, bot):
        self.ready_called = True

    async def on_message(self, bot, message):
        self.message_called_with.append(message)


class TestIntegrationTwitchBot(IsolatedAsyncioTestCase):

    async def test__ready_event_dispatches_to_plugin__no_errors(self):
        plugin = TestPlugin()

        dispatcher = EventDispatcher([plugin])

        bot = TwitchBot(
            token="fake_token",
            channels_to_connect=["channels_to_connect"],
            twitch_secret_key="secret",
            event_dispatcher=dispatcher,
        )

        await bot.event_ready()

        assert plugin.ready_called is True

    async def test__on_message_event_dispatches_to_plugin__no_errors(self):
        plugin = TestPlugin()
        dispatcher = EventDispatcher([plugin])

        bot = TwitchBot(
            token="fake_token",
            channels_to_connect=["channels_to_connect"],
            twitch_secret_key="secret",
            event_dispatcher=dispatcher,
        )

        message = MagicMock()
        message.content = "message_content"

        await bot.event_message(message)

        assert plugin.message_called_with == [message]
