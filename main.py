import os
import logging

from dotenv import load_dotenv
from twitch_bot.ai.ai_ollama_service import AIOllamaService
from twitch_bot.event_dispatchers.event_dispatcher import EventDispatcher
from twitch_bot.plugins.ai_ask_bot_plugin import AIAskPlugin
from twitch_bot.plugins.ai_persona_plugin import AIPersonaPlugin
from twitch_bot.plugins.ai_question_spam_bot_plugin import AIQuestionSpamPlugin
from twitch_bot.plugins.console_chat_bot_plugin import ConsoleChatBotPlugin
from twitch_bot.plugins.helpers import DurationRange
from twitch_bot.plugins.log_start_bot_plugin import LogStartBotPlugin
from twitch_bot.plugins.periodic_spam_bot_plugin import PeriodicSpamBotPlugin
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

ai_service = AIOllamaService(model="phi3")

plugins = [
    LogStartBotPlugin(),
    ConsoleChatBotPlugin(target_channels=["2", "3"]),
    PeriodicSpamBotPlugin(messages=["PERIOD"], interval=DurationRange(5, 5)),
]

event_dispatcher = EventDispatcher(plugins)

# TODO подумать над подключенными каналами, все плагины кроме консоли
# работают на всех каналах
bot = TwitchBot(
    token=TWITCH_TOKEN_AOTH,
    channels_to_connect=["alduin3115", "pudgeforever4"],
    twitch_secret_key=TWITCH_SECRET_KEY,
    event_dispatcher=event_dispatcher,
)

if __name__ == "__main__":
    bot.run()
