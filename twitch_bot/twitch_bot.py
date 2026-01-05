from twitchio.ext import commands
from twitch_bot.plugin_managers.plugin_manager import IPluginManager


class TwitchBot(commands.Bot):
    def __init__(
        self,
        token: str,
        channels_to_connect: list[str],
        twitch_secret_key: str,
        plugin_manager: IPluginManager,
    ):
        super().__init__(
            token=token,
            prefix="?",
            client_secret=twitch_secret_key,
            initial_channels=channels_to_connect,
        )
        self.plugin_manager = plugin_manager

    async def event_ready(self):
        print(f"[Bot] Logged in as {self.nick}")
        await self.plugin_manager.on_ready(self)

    async def event_message(self, message):
        await self.plugin_manager.on_message(self, message)

    async def event_raw_data(self, data):
        await self.plugin_manager.on_raw(self, data)
