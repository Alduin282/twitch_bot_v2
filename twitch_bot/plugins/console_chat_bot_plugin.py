import asyncio
import logging

from twitch_bot.definitions import EVENT_HANDLER, EventType
from twitch_bot.twitch_bot import TwitchBot
from twitch_bot.plugins.bot_plugin import BotPlugin
from twitchio import Channel


logger = logging.getLogger(__name__)


class ConsoleChatBotPlugin(BotPlugin):

    def __init__(self, target_channels: list[str] | None = None) -> None:
        self._target_channels = target_channels or []

    def get_event_handlers(self) -> dict[EventType, EVENT_HANDLER]:
        return {
            EventType.READY: self._on_ready,
        }

    async def _on_ready(self, bot: TwitchBot) -> None:
        asyncio.create_task(self._start_console_chat_loop(bot))

    async def _start_console_chat_loop(self, bot: TwitchBot):
        channels_to_chat = self._get_channels(bot)
        if not channels_to_chat:
            logger.error(
                (
                    "[ConsoleChatBotPlugin] "
                    "No channels to chat is taken. Plugin is not started"
                )
            )
            return

        while True:
            message = await asyncio.to_thread(input, "Your message: ")

            for channel in channels_to_chat:
                await channel.send(message)

    def _get_channels(self, bot: TwitchBot) -> list[Channel]:
        if self._target_channels:
            return self._resolve_target_channels(bot)

        return bot.connected_channels

    def _resolve_target_channels(self, bot: TwitchBot) -> list[Channel]:
        channels: list[Channel] = []

        for channel_name in self._target_channels:
            channel = bot.get_channel(channel_name)

            if channel is None:
                logger.warning(
                    (
                        "[ConsoleChatBotPlugin]"
                        f" Channel '{channel_name}' not found among connected channels"
                    )
                )
                continue

            channels.append(channel)

        if not channels:
            logger.error(
                (
                    "[ConsoleChatBotPlugin] "
                    "None of the target channels were found among connected channels. "
                    "Plugin is not sending messages anywhere"
                )
            )

        return channels
