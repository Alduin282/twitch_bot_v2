from typing import Sequence
from twitchio import Message
from twitch_bot.plugin_managers.interface_plugin_manager import IPluginManager
from twitch_bot.plugins.bot_plugin import BotPlugin
from twitch_bot.twitch_bot import TwitchBot


class PluginManager(IPluginManager):
    def __init__(self, bot_plugins: Sequence[BotPlugin]) -> None:
        self.bot_plugins = bot_plugins

    async def on_ready(self, bot: TwitchBot) -> None:
        for plugin in self.bot_plugins:
            await plugin.on_ready(bot)

    async def on_message(self, bot: TwitchBot, message: Message) -> None:
        for plugin in self.bot_plugins:
            await plugin.on_message(bot, message)

    async def on_raw(self, bot: TwitchBot, raw_data: str) -> None:
        for plugin in self.bot_plugins:
            await plugin.on_raw(bot, raw_data)
