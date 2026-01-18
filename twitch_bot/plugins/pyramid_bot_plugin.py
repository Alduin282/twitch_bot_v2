from twitch_bot.definitions import EVENT_HANDLER, EventType
from twitch_bot.twitch_bot import TwitchBot
from twitch_bot.plugins.bot_plugin import BotPlugin
from twitchio import Message


class PyramidBotPlugin(BotPlugin):
    # TODO дать возможность задавать смайл пирамиды, если нет юзаем дефолтный
    # TODO список конретных пользаков , которые могут спамить этой темой
    COMMAND = "pyramid"
    NO_PYRAMID_HEIGHT_MESSAGE = "высота пирамиды не задана"
    PYRAMID_HEIGHT_IS_NOT_NUMBER_MESSAGE = "высота пирамиды не задана"
    PYRAMID_HEIGHT_LESS_MINIMUM_MESSAGE = "высота пирмаиды меньше минимальной"
    PYRAMID_HEIGHT_MORE_MAXIMUM_MESSAGE = "высота пирамиды больше максимальной"
    MAXIMUM_PYRAMID_HEIGHT = 10
    MINIMUM_PYRAMID_HEIGHT = 2
    DEFAULT_PYRAMID_SMILE = "LUL"

    def get_event_handlers(self) -> dict[EventType, EVENT_HANDLER]:
        return {
            EventType.MESSAGE: self._on_message,
        }

    async def _on_message(self, bot: TwitchBot, message: Message) -> None:
        text_of_command = message.content or ""
        if not text_of_command.startswith(self.COMMAND):
            return

        channel = message.channel

        ok, problem_message = self._validate_pyramid_command(text_of_command)
        if not ok:
            await channel.send(f"@{message.author.name} {problem_message}")
            return

        pyramid_height = self._get_pyramid_height(text_of_command)
        for pyramid_line in self._build_pyramid(pyramid_height):
            await channel.send(pyramid_line)

    def _validate_pyramid_command(self, text_of_command: str) -> tuple[bool, str]:
        parts_of_command = text_of_command.split()

        if len(parts_of_command) < 2:
            return False, self.NO_PYRAMID_HEIGHT_MESSAGE

        try:
            pyramid_height = int(parts_of_command[1])
        except ValueError:
            return False, self.PYRAMID_HEIGHT_IS_NOT_NUMBER_MESSAGE

        if pyramid_height < self.MINIMUM_PYRAMID_HEIGHT:
            return False, self.PYRAMID_HEIGHT_LESS_MINIMUM_MESSAGE

        if pyramid_height > self.MAXIMUM_PYRAMID_HEIGHT:
            return False, self.PYRAMID_HEIGHT_MORE_MAXIMUM_MESSAGE

        return True, ""

    def _build_pyramid(self, pyramid_height: int) -> list[str]:
        pyramid = []

        for i in range(1, pyramid_height * 2):
            current_level = i if i <= pyramid_height else pyramid_height * 2 - i
            pyramid.append((f"{self.DEFAULT_PYRAMID_SMILE} " * current_level).strip())

        return pyramid

    @staticmethod
    def _get_pyramid_height(text_of_command: str) -> int:
        return int(text_of_command.split()[1])
