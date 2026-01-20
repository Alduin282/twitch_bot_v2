from twitch_bot.ai.ai_ollama_service import AIOllamaService
from twitch_bot.definitions import EVENT_HANDLER, EventType
from twitch_bot.plugins.bot_plugin import BotPlugin
from twitch_bot.plugins.helpers import Cooldown
from twitchio import Message
from twitch_bot.twitch_bot import TwitchBot


class AIAskPlugin(BotPlugin):
    NO_QUESTION_ANSWER = "Нужно указать вопрос 😊 Пример: !ask как дела?"

    def __init__(self, ai_service: AIOllamaService, cooldown_seconds: int = 30) -> None:
        self._ai = ai_service
        self._cooldown_seconds = cooldown_seconds
        self._cooldowns: dict[str, Cooldown] = {}

    def get_event_handlers(self) -> dict[EventType, EVENT_HANDLER]:
        return {
            EventType.MESSAGE: self._on_message,
        }

    async def _on_message(self, bot: TwitchBot, message: Message) -> None:
        content = (message.content or "").strip()
        if not content.startswith("!ask"):
            return

        channel = message.channel
        cooldown = self._get_channel_cooldown(channel.name)
        if not cooldown.is_ready():
            return

        question = content[4:].strip()
        if not question:
            await channel.send(self.NO_QUESTION_ANSWER)
            return

        answer = await self._ai.answer(question)
        await channel.send(answer[:500])

    def _get_channel_cooldown(self, channel_name: str) -> Cooldown:
        return self._cooldowns.setdefault(
            channel_name, Cooldown(self._cooldown_seconds)
        )
