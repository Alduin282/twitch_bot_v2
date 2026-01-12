import asyncio
import logging
import random

from twitch_bot.definitions import EVENT_HANDLER, EventType
from twitch_bot.plugins.helpers import Cooldown
from twitch_bot.twitch_bot import TwitchBot
from twitch_bot.plugins.bot_plugin import BotPlugin
from twitchio import Message

logger = logging.getLogger(__name__)


class LaughReactionBotPlugin(BotPlugin):
    LAUGH_TRIGGERS = (
        "LUL",
        "))",
        "LOL",
        "LO",
        "ахах",
        "пхпх",
        "ахпх",
        "f[f[",
        "хаха",
        "АХАХ",
        "ХАХА",
    )
    LAUGH_REPLIES = (
        "ахаххаха",
        "f[f[[f[f[f[[f",
        "АХХАХАХАХА",
        "ПХАХАХПХХАХ",
        "хахахахаха",
        "ХАХАХАХХААХ",
        "ahahahahha",
        "AHAHHAHAHAH",
        "LUL",
        "ахах",
        "хахаахах",
        "аххаха",
        "ахаххахах BloodTrail",
        "LOL",
        "LO",
        "))",
        "LOL LOL",
        "LO LO",
        "ржака",
        "забавно))",
        "LOL ))",
        ")) ))",
    )

    def __init__(self, cooldown_seconds: float = 10) -> None:
        self._cooldown_seconds = cooldown_seconds
        self._cooldowns: dict[str, Cooldown] = {}

    def get_event_handlers(self) -> dict[EventType, EVENT_HANDLER]:
        return {
            EventType.MESSAGE: self._on_message,
        }

    async def _on_message(self, bot: TwitchBot, message: Message) -> None:
        channel_name = message.channel.name
        cooldown = self._get_channel_cooldown(channel_name)
        if not cooldown.is_ready():
            return

        text_of_message = message.content or ""
        if not any(
            text_of_message.startswith(trigger) for trigger in self.LAUGH_TRIGGERS
        ):
            return

        # чуть ждем, чтобы ответ не был слишком резким
        await asyncio.sleep(random.uniform(0.3, 1.0))
        await message.channel.send(random.choice(self.LAUGH_REPLIES))
        cooldown.trigger()

    def _get_channel_cooldown(self, channel_name: str) -> Cooldown:
        return self._cooldowns.setdefault(
            channel_name, Cooldown(self._cooldown_seconds)
        )
