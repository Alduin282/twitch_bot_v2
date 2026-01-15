import random

from dataclasses import dataclass, field
from uuid import uuid4
from twitch_bot.definitions import EVENT_HANDLER, EventType
from twitch_bot.plugins.bot_plugin import BotPlugin
from twitch_bot.plugins.helpers import Cooldown, DurationRange, sleep_in_range
from twitch_bot.twitch_bot import TwitchBot
from twitchio import Message


@dataclass
class ReactionRule:
    triggers: tuple[str, ...]
    replies: tuple[str, ...]
    reaction_probability: float
    ignore_echo: bool
    cooldown_seconds: float
    pre_reaction_delay: DurationRange
    _uid: str = field(default_factory=lambda: str(uuid4()), init=False)

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


class ReactionBotPlugin(BotPlugin):
    def __init__(
        self,
        triggers: tuple[str, ...],
        replies: tuple[str, ...],
        reaction_probability: float = 1.0,
        ignore_echo: bool = True,
        cooldown_seconds: float = 10,
        pre_reaction_delay_max: float = 0,
        pre_reaction_delay_min: float = 0,
    ) -> None:
        self.reaction_rule = ReactionRule(
            triggers=triggers,
            replies=replies,
            reaction_probability=reaction_probability,
            ignore_echo=ignore_echo,
            cooldown_seconds=cooldown_seconds,
            pre_reaction_delay=DurationRange(
                pre_reaction_delay_min, pre_reaction_delay_max
            ),
        )
        self._cooldowns: dict[str, Cooldown] = {}

    def get_event_handlers(self) -> dict[EventType, EVENT_HANDLER]:
        return {EventType.MESSAGE: self._on_message}

    async def _on_message(self, bot: TwitchBot, message: Message) -> None:
        if not self._should_react(self.reaction_rule, message):
            return

        cooldown = self._get_channel_cooldown(message.channel.name)
        if not cooldown.is_ready():
            return

        await self._react_with_delay(message, self.reaction_rule)
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

    def _get_channel_cooldown(self, channel_name: str) -> Cooldown:
        return self._cooldowns.setdefault(
            channel_name, Cooldown(self.reaction_rule.cooldown_seconds)
        )

    @staticmethod
    async def _react_with_delay(message: Message, reaction_rule: ReactionRule) -> None:
        await sleep_in_range(reaction_rule.pre_reaction_delay)
        await message.channel.send(random.choice(reaction_rule.replies))
