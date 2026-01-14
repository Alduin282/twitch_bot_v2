import asyncio
import logging

from twitch_bot.ai.ai_ollama_service import AIOllamaService
from twitch_bot.definitions import EVENT_HANDLER, EventType
from twitch_bot.plugins.helpers import DurationRange, sleep_in_range
from twitch_bot.twitch_bot import TwitchBot
from twitch_bot.plugins.bot_plugin import BotPlugin

logger = logging.getLogger(__name__)


class AIQuestionSpamPlugin(BotPlugin):
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
                stream_context = await self._build_stream_context(bot, channel.name)

                question = await self._ai_service.ask_streamer(stream_context)
                # Twitch safety
                question = question[:499]

                await channel.send(question)

    async def _build_stream_context(self, bot: TwitchBot, channel_name: str) -> str:
        streams = await bot.fetch_streams(user_logins=[channel_name])
        if not streams:
            return ""

        stream = streams[0]

        title = stream.title or "Стрим без названия"
        game = stream.game_name or "Игра не указана"

        if stream.tags:
            tags = ", ".join(stream.tags)
        else:
            tags = "нет тегов"

        context = f"Заголовок стрима: {title}. " f"Теги: {tags}. " f"Игра: {game}."

        return context
