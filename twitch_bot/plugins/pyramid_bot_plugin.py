from twitch_bot.definitions import EVENT_HANDLER, EventType
from twitch_bot.twitch_bot import TwitchBot
from twitch_bot.plugins.bot_plugin import BotPlugin
from twitchio import Message


class PyramidBotPlugin(BotPlugin):
    COMMAND_NAME = "pyramid"
    NO_PYRAMID_LEVEL_MESSAGE = ""
    PYRAMID_LEVEL_IS_NOT_NUMBER_MESSAGE = "высота пирамиды не задана"
    PYRAMID_LEVEL_LESS_MINIMUM_MESSAGE = "высота пирмаиды меньше минимальной"
    PYRAMID_LEVEL_MORE_MAXIMUM_MESSAGE = "высота пирамиды больше максимальной"
    MAXIMUM_PYRAMID_LEVEL = 10
    MINIMUM_PYRAMID_LEVEL = 2
    DEFAULT_PYRAMID_SMILE = "LUL"

    def get_event_handlers(self) -> dict[EventType, EVENT_HANDLER]:
        return {
            EventType.MESSAGE: self._on_message,
        }

    async def _on_message(self, bot: TwitchBot, message: Message) -> None:
        text_of_command = message.content or ""
        if not text_of_command.startswith(self.COMMAND_NAME):
            return

        context_of_command = await bot.get_context(message)

        ok, problem_message = self._validate_pyramid_command(text_of_command)
        if not ok:
            await context_of_command.send(f"@{message.author.name} {problem_message}")
            return

        pyramid_level = self._get_pyramid_level(text_of_command)
        for pyramid_line in self._build_pyramid(pyramid_level):
            await context_of_command.send(pyramid_line)

    def _validate_pyramid_command(self, text_of_command: str) -> tuple[bool, str]:
        parts_of_command = text_of_command.split()

        if len(parts_of_command) < 2:
            return False, self.NO_PYRAMID_LEVEL_MESSAGE

        try:
            pyramid_level = int(parts_of_command[1])
        except ValueError:
            return False, self.PYRAMID_LEVEL_IS_NOT_NUMBER_MESSAGE

        if pyramid_level < self.MINIMUM_PYRAMID_LEVEL:
            return False, self.PYRAMID_LEVEL_LESS_MINIMUM_MESSAGE

        if pyramid_level > self.MAXIMUM_PYRAMID_LEVEL:
            return False, self.PYRAMID_LEVEL_MORE_MAXIMUM_MESSAGE

        return True, ""

    def _build_pyramid(self, pyramid_level: int) -> list[str]:
        pyramid = []

        for i in range(1, pyramid_level * 2):
            current_level = i if i <= pyramid_level else pyramid_level * 2 - i
            pyramid.append((f"{self.DEFAULT_PYRAMID_SMILE} " * current_level).strip())

        return pyramid

    @staticmethod
    def _get_pyramid_level(text_of_command: str) -> int:
        return int(text_of_command.split()[1])
