import os

from dotenv import load_dotenv
from twitch_bot.plugin_managers.plugin_manager import PluginManager
from twitch_bot.plugins.empty_plugin import EmptyBotPlugin
from twitch_bot.twitch_bot import TwitchBot

load_dotenv()

TWITCH_TOKEN_AOTH = os.getenv("TWITCH_TOKEN_AOTH_ALDUIN")
if TWITCH_TOKEN_AOTH is None:
    raise RuntimeError("Twitch token is not found")

TWITCH_SECRET_KEY = os.getenv("TWITCH_SECRET_KEY_ALDUIN")
if TWITCH_SECRET_KEY is None:
    raise RuntimeError("Twitch secret key is not found")

plugins = [
    EmptyBotPlugin(),
]

manager = PluginManager(plugins)

bot = TwitchBot(
    token=TWITCH_TOKEN_AOTH,
    channels_to_connect=["alduin3115"],
    twitch_secret_key=TWITCH_SECRET_KEY,
    plugin_manager=manager,
)

bot.run()
