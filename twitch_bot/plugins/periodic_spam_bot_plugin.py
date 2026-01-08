import asyncio
import logging
import random
from typing import Sequence
from twitch_bot.definitions import EVENT_HANDLER, EventType
from twitch_bot.plugins.helpers import DurationRange
from twitch_bot.twitch_bot import TwitchBot
from twitch_bot.plugins.bot_plugin import BotPlugin

logger = logging.getLogger(__name__)


class PeriodicSpamBotPlugin(BotPlugin):

    def __init__(
        self,
        messages: Sequence[str],
        interval: DurationRange,
        delay_start_seconds: float = 0.0,
    ) -> None:
        if not messages:
            raise ValueError("messages cannot be empty")

        if delay_start_seconds < 0:
            raise ValueError("delay_start_seconds must be >= 0")

        self._messages = messages
        self._interval = interval
        self._delay_start_seconds = delay_start_seconds

    def get_event_handlers(self) -> dict[EventType, EVENT_HANDLER]:
        return {
            EventType.READY: self._on_ready,
        }

    async def _on_ready(self, bot: TwitchBot) -> None:
        if self._delay_start_seconds > 0:
            await asyncio.sleep(self._delay_start_seconds)

        channels = bot.connected_channels
        if not channels:
            logger.warning(
                "[PeriodicSpamBotPlugin]: no connected channels, skipping spam"
            )
            return

        while True:
            await self._interval.sleep_in_range()
            message = random.choice(self._messages)

            for channel in channels:
                await channel.send(message)
