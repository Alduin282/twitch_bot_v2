import asyncio
import random

from dataclasses import dataclass, field
from typing import Sequence
from uuid import uuid4
from twitch_bot.definitions import EVENT_HANDLER, EventType
from twitch_bot.plugins.bot_plugin import BotPlugin
from twitch_bot.plugins.helpers import Cooldown, Delay
from twitch_bot.twitch_bot import TwitchBot
from twitchio import Message


@dataclass
class ReactionRule:
    triggers: Sequence[str]
    replies: Sequence[str]
    reaction_probability: float = 1.0
    ignore_echo: bool = True
    cooldown_seconds: float = 10
    pre_reaction_delay: Delay = field(default_factory=Delay)
    _uid: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self):
        if not (0.0 <= self.reaction_probability <= 1.0):
            raise ValueError(
                "reaction_probability must be between 0 and 1, "
                f"got {self.reaction_probability}"
            )

        if self.cooldown_seconds < 0:
            raise ValueError(
                f"cooldown_seconds must be >= 0, got {self.cooldown_seconds}"
            )

        if not self.triggers:
            raise ValueError("ReactionRule must have at least one trigger")
        if not self.replies:
            raise ValueError("ReactionRule must have at least one reply")


class ReactionPlugin(BotPlugin):
    def __init__(self, reaction_rules: list[ReactionRule]) -> None:
        self.reaction_rules = reaction_rules
        self._cooldowns: dict[tuple[str, str], Cooldown] = {}

    def get_event_handlers(self) -> dict[EventType, EVENT_HANDLER]:
        return {EventType.MESSAGE: self._on_message}

    async def _on_message(self, bot: TwitchBot, message: Message) -> None:
        for rule in self.reaction_rules:
            if not self._should_react(rule, message):
                continue

            cooldown = self._get_cooldown(message.channel.name, rule)
            if not cooldown.is_ready():
                continue

            asyncio.create_task(self._react_with_delay(message, rule))
            cooldown.trigger()
            return

    @staticmethod
    def _should_react(reaction_rule: ReactionRule, message: Message) -> bool:
        words_of_content = (message.content or "").split()

        if reaction_rule.ignore_echo and message.echo:
            return False
        if not any(t in words_of_content for t in reaction_rule.triggers):
            return False
        if random.random() > reaction_rule.reaction_probability:
            return False
        return True

    def _get_cooldown(self, channel_name: str, reaction_rule: ReactionRule) -> Cooldown:
        key = (channel_name, reaction_rule._uid)
        return self._cooldowns.setdefault(key, Cooldown(reaction_rule.cooldown_seconds))

    async def _react_with_delay(self, message: Message, reaction_rule: ReactionRule):
        if reaction_rule.pre_reaction_delay.should_delay():
            await reaction_rule.pre_reaction_delay.wait()
        await message.channel.send(random.choice(reaction_rule.replies))
