import asyncio
import logging

from typing import Optional
from twitch_bot.ai.ai_ollama_service import AIOllamaService
from twitch_bot.definitions import EVENT_HANDLER, EventType
from twitch_bot.plugins.helpers import DurationRange, sleep_in_range
from twitch_bot.twitch_bot import TwitchBot
from twitch_bot.plugins.bot_plugin import BotPlugin
from twitchio.models import Stream

logger = logging.getLogger(__name__)


class AIQuestionSpamPlugin(BotPlugin):
    NO_TAGS = "нет тегов"
    NO_TITLE = "Стрим без названия"
    NO_GAME_NAME = "Игра не указана"

    def __init__(
        self,
        ai_service: AIOllamaService,
        interval: DurationRange,
        delay_start_seconds: float = 0.0,
    ):
        self._ai_service = ai_service
        self._interval = interval
        self._delay_start_seconds = delay_start_seconds

    def get_event_handlers(self) -> dict[EventType, EVENT_HANDLER]:
        return {
            EventType.READY: self._on_ready,
        }

    async def _on_ready(self, bot: TwitchBot) -> None:
        if self._delay_start_seconds > 0:
            await asyncio.sleep(self._delay_start_seconds)

        while True:
            connected_channels = bot.connected_channels
            if not connected_channels:
                logger.warning("[AIQuestionSpamPlugin]: no channels, stopping loop")
                return

            await sleep_in_range(self._interval)

            for channel in connected_channels:
                stream = await self._get_stream(bot, channel.name)
                stream_context = self._build_stream_context(stream)

                question = await self._ai_service.ask_streamer(stream_context)
                question = question[:500]

                await channel.send(question)

    async def _get_stream(self, bot: TwitchBot, channel_name: str) -> Optional[Stream]:
        streams = await bot.fetch_streams(user_logins=[channel_name])
        if not streams:
            return None
        return streams[0]

    def _build_stream_context(self, stream: Stream | None) -> str:
        if not stream:
            return ""

        title = stream.title or self.NO_TITLE
        game = stream.game_name or self.NO_GAME_NAME

        if stream.tags:
            tags = ", ".join(stream.tags)
        else:
            tags = self.NO_TAGS

        context = f"Заголовок стрима: {title}. " f"Теги: {tags}. " f"Игра: {game}."

        return context
