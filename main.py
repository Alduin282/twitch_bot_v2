import os
import logging

from dotenv import load_dotenv
from twitch_bot.event_dispatchers.event_dispatcher import EventDispatcher
from twitch_bot.plugins.helpers import DurationRange
from twitch_bot.plugins.log_start_bot_plugin import LogStartBotPlugin
from twitch_bot.plugins.reaction_bot_plugin import ReactionPlugin, ReactionRule
from twitch_bot.twitch_bot import TwitchBot

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

TWITCH_TOKEN_AOTH = os.getenv("TWITCH_TOKEN_AOTH_ALDUIN")
if TWITCH_TOKEN_AOTH is None:
    raise RuntimeError("Twitch token is not found")

TWITCH_SECRET_KEY = os.getenv("TWITCH_SECRET_KEY_ALDUIN")
if TWITCH_SECRET_KEY is None:
    raise RuntimeError("Twitch secret key is not found")

plugins = [
    LogStartBotPlugin(),
    ReactionPlugin(
        reaction_rules=[
            ReactionRule(
                triggers=["FUCK"],
                replies=["ТЫ ДОЛБАЕБ?", "ТИШЕ ТИШЕ"],
                ignore_echo=False,
                pre_reaction_delay=DurationRange(10, 10),
                cooldown_seconds=20,
            ),
            ReactionRule(
                triggers=["HEHE"],
                replies=["LOL?"],
                ignore_echo=False,
                cooldown_seconds=0,
            ),
        ]
    ),
]


event_dispatcher = EventDispatcher(plugins)

bot = TwitchBot(
    token=TWITCH_TOKEN_AOTH,
    channels_to_connect=["alduin3115", "pudgeforever4"],
    twitch_secret_key=TWITCH_SECRET_KEY,
    event_dispatcher=event_dispatcher,
)

if __name__ == "__main__":
    bot.run()
