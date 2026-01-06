from typing import Callable
from twitch_bot.definitions import EventType
from twitch_bot.twitch_bot import TwitchBot
from twitch_bot.plugins.bot_plugin import BotPlugin


class EmptyBotPlugin(BotPlugin):

    async def on_ready(self, bot: TwitchBot) -> None:
        print("[EmptyPlugin] bot ready, happy bot")

    def get_event_handlers(self) -> dict[EventType, Callable]:
        return {
            EventType.READY: self.on_ready,
        }
