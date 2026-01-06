from twitch_bot.definitions import EventHandler, EventType
from twitch_bot.twitch_bot import TwitchBot
from twitch_bot.plugins.bot_plugin import BotPlugin
import logging

logger = logging.getLogger(__name__)


class LogStartBotPlugin(BotPlugin):

    async def on_ready(self, bot: TwitchBot) -> None:
        logger.info(f"[LogStartBotPlugin] Logged in as {bot.nick}")
        logger.info(f"[LogStartBotPlugin] User id is {bot.user_id}")

    def get_event_handlers(self) -> dict[EventType, EventHandler]:
        return {
            EventType.READY: self.on_ready,
        }
