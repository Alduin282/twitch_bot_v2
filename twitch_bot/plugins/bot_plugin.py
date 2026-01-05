from abc import ABC
from twitchio import Message

from twitch_bot.twitch_bot import TwitchBot


class BotPlugin(ABC):

    async def on_ready(self, bot: TwitchBot) -> None:
        pass

    async def on_message(self, bot: TwitchBot, message: Message) -> None:
        pass

    async def on_raw(self, bot: TwitchBot, raw_data: str) -> None:
        pass
