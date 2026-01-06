from twitchio.ext import commands
from twitch_bot.definitions import EventType
from twitch_bot.plugin_managers.event_dispatcher import EventDispatcher


class TwitchBot(commands.Bot):
    def __init__(
        self,
        token: str,
        channels_to_connect: list[str],
        twitch_secret_key: str,
        event_dispatcher: EventDispatcher,
    ):
        super().__init__(
            token=token,
            prefix="?",
            client_secret=twitch_secret_key,
            initial_channels=channels_to_connect,
        )
        self.event_dispatcher = event_dispatcher

    async def event_ready(self):
        print(f"[Bot] Logged in as {self.nick}")  # это бы отсюда убрать
        await self.event_dispatcher.dispatch(EventType.READY, self)

    async def event_message(self, message):
        await self.event_dispatcher.dispatch(EventType.MESSAGE, self, message)
