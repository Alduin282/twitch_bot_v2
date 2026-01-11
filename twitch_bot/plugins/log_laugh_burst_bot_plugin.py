import asyncio
import logging

from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Sequence
from twitchio import Message

from twitch_bot.definitions import EVENT_HANDLER, EventType
from twitch_bot.plugins.helpers import Cooldown
from twitch_bot.twitch_bot import TwitchBot
from twitch_bot.plugins.bot_plugin import BotPlugin


logger = logging.getLogger(__name__)


@dataclass
class LaughRule:
    laugh_markers: Sequence[str]
    window_size_messages: int
    required_matches: int
    cooldown_seconds: int
    log_file: str

    def __post_init__(self):
        if not self.laugh_markers:
            raise ValueError("laugh_markers cannot be empty")

        if self.window_size_messages <= 0:
            raise ValueError("window_size_messages must be > 0")

        if self.required_matches <= 0:
            raise ValueError("required_matches must be > 0")

        if self.required_matches > self.window_size_messages:
            raise ValueError("required_matches cannot exceed window_size_messages")

        if self.cooldown_seconds < 0:
            raise ValueError("cooldown_seconds must be >= 0")


class LogLaughBurstBotPlugin(BotPlugin):
    def __init__(
        self,
        laugh_markers: Sequence[str] = ("ахаа", "хаха", "lul", "lol", "lo "),
        window_size_messages: int = 10,
        required_matches: int = 6,
        cooldown_seconds: int = 180,
        log_file: str = "twitch_burst_log.txt",
    ) -> None:
        self.laugh_rule = LaughRule(
            laugh_markers=laugh_markers,
            window_size_messages=window_size_messages,
            required_matches=required_matches,
            cooldown_seconds=cooldown_seconds,
            log_file=log_file,
        )
        self._file_lock = asyncio.Lock()
        self._cooldowns: dict[str, Cooldown] = {}
        self.window_messages_state: dict[str, deque] = {}

    def get_event_handlers(self) -> dict[EventType, EVENT_HANDLER]:
        return {
            EventType.MESSAGE: self._on_message,
        }

    async def _on_message(self, bot: TwitchBot, message: Message) -> None:
        channel_name = message.channel.name
        cooldown = self._get_channel_cooldown(channel_name)

        self.window_messages_state.setdefault(
            channel_name,
            deque(maxlen=self.laugh_rule.window_size_messages),
        )
        message_text = (message.content or "").lower()
        channel_state = self.window_messages_state[channel_name]
        channel_state.append(message_text)

        if not self._should_log(message_text, channel_state, cooldown):
            return

        await self._log_laugh(channel_name, message.timestamp, bot)
        cooldown.trigger()

    def _get_channel_cooldown(self, channel_name: str) -> Cooldown:
        return self._cooldowns.setdefault(
            channel_name, Cooldown(self.laugh_rule.cooldown_seconds)
        )

    def _should_log(
        self, message_text: str, channel_state: deque, cooldown: Cooldown
    ) -> bool:
        if not self._is_laugh(message_text):
            return False

        if not self._has_laugh_burst(channel_state):
            return False

        if not cooldown.is_ready():
            return False

        return True

    def _is_laugh(self, text: str) -> bool:
        return any(marker in text for marker in self.laugh_rule.laugh_markers)

    def _has_laugh_burst(self, messages: deque[str]) -> bool:
        count_laugh_messages = sum(1 for message in messages if self._is_laugh(message))
        return count_laugh_messages >= self.laugh_rule.required_matches

    async def _log_laugh(
        self, channel_name: str, message_timestamp: datetime, bot: TwitchBot
    ) -> None:
        stream_start = await self._get_start_stream_time(bot, channel_name)
        if not stream_start:
            return

        message_timestamp_utc = message_timestamp.replace(tzinfo=timezone.utc)
        stream_time = message_timestamp_utc - stream_start

        log_line = (
            f"{channel_name} LAUGH-BURST at {message_timestamp} ({stream_time})\n"
        )
        try:
            await asyncio.to_thread(self._append_log, log_line)
            logger.info("[LogLaughBurstBotPlugin] laugh burst log successfully added")
        except Exception as e:
            logger.error(f"[LogLaughBurstBotPlugin] Failed to write laugh log: {e}")

    @staticmethod
    async def _get_start_stream_time(
        bot: TwitchBot, channel_name: str
    ) -> Optional[datetime]:
        try:
            streams = await bot.fetch_streams(user_logins=[channel_name])

            if not streams:
                logger.warning(
                    f"[LogLaughBurstBotPlugin] No active stream"
                    f" found for '{channel_name}'"
                )
                return None

            stream = streams[0]
            return stream.started_at
        except Exception as e:
            logger.error(
                f"[LogLaughBurstBotPlugin] Failed to fetch stream start time "
                f"for '{channel_name}': {e}"
            )
            return None

    def _append_log(self, log_line: str):
        with open(self.laugh_rule.log_file, "a", encoding="utf-8") as f:
            f.write(log_line)
