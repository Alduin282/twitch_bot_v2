from twitch_bot.ai.ai_ollama_service import AIOllamaService
from twitch_bot.definitions import EVENT_HANDLER, EventType
from twitch_bot.plugins.bot_plugin import BotPlugin
from twitchio import Message
from twitch_bot.twitch_bot import TwitchBot


# FIXME не корректно работает с несколькими канаалми
# поменяв персону на одном канале, меняется на всех
class AIPersonaPlugin(BotPlugin):
    PREFIX = "!persona"
    GET_PERSONA_COMMAND = f"{PREFIX}"
    RANDOM_PERSONA_COMMAND = f"{PREFIX} random"
    RESET_PERSONA_COMMAND = f"{PREFIX} reset"

    def __init__(self, ai_service: AIOllamaService):
        self._ai = ai_service

    def get_event_handlers(self) -> dict[EventType, EVENT_HANDLER]:
        return {
            EventType.MESSAGE: self._on_message,
        }

    async def _on_message(self, bot: TwitchBot, message: Message) -> None:
        content = (message.content or "").strip()

        command_handlers = {
            self.GET_PERSONA_COMMAND: self._handle_show_persona,
            self.RANDOM_PERSONA_COMMAND: self._handle_random,
            self.RESET_PERSONA_COMMAND: self._handle_reset,
        }

        command_handler = command_handlers.get(content)
        if command_handler:
            await command_handler(message)

    async def _handle_show_persona(self, message: Message):
        persona = self._ai.get_persona()
        await message.channel.send(persona[:500])

    async def _handle_random(self, message: Message):
        if not self._is_author_mod(message):
            return

        await self._ai.set_random_persona()
        await message.channel.send("Персона обновлена 🤖")

    async def _handle_reset(self, message: Message):
        if not self._is_author_mod(message):
            return

        self._ai.reset_persona()
        await message.channel.send("Персона сброшена 🧹")

    def _is_author_mod(self, message: Message) -> bool:
        return getattr(message.author, "is_mod", False)
