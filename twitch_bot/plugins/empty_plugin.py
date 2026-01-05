from twitch_bot.twitch_bot import TwitchBot
from twitch_bot.plugins.bot_plugin import BotPlugin


class EmptyBotPlugin(BotPlugin):
    async def on_ready(self, bot: TwitchBot) -> None:
        print("[EmptyPlugin] on_ready, happy bot")
