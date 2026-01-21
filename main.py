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
from twitch_bot.plugins.laugh_reaction_bot_plugin import LaughReactionBotPlugin
from twitch_bot.plugins.log_laugh_burst_bot_plugin import LogLaughBurstBotPlugin
from twitch_bot.plugins.log_start_bot_plugin import LogStartBotPlugin
from twitch_bot.plugins.periodic_spam_bot_plugin import PeriodicSpamBotPlugin
from twitch_bot.plugins.pyramid_bot_plugin import PyramidBotPlugin
from twitch_bot.plugins.reaction_bot_plugin import ReactionBotPlugin
from twitch_bot.twitch_bot import TwitchBot

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

# Положите токен и секрет в .env прерд запуском
TWITCH_TOKEN_AOTH = os.getenv("TWITCH_TOKEN_AOTH_ALDUIN")
if TWITCH_TOKEN_AOTH is None:
    raise RuntimeError("Twitch token is not found. Добавьте его в .env")

TWITCH_SECRET_KEY = os.getenv("TWITCH_SECRET_KEY_ALDUIN")
if TWITCH_SECRET_KEY is None:
    raise RuntimeError("Twitch secret не найден. Добавьте его в .env")

# ИИ сервис, если будете исползовать ИИ плагины, можно выбрать любую модель Ollama
# Нужна локально запущенная Ollama
ai_service = AIOllamaService(model="phi3")

# Добавляйте и кастомизируйет плагины которые собираетесь использовать
# Можно запустить несколько одинаковых
plugins = [
    LogStartBotPlugin(),
    # AIAskPlugin(ai_service=ai_service, cooldown_seconds=30),
    # AIPersonaPlugin(ai_service),
    # AIQuestionSpamPlugin(
    #     ai_service,
    #     interval=DurationRange(min_seconds=60, max_seconds=600),
    #     delay_start_seconds=60,
    # ),
    # ConsoleChatBotPlugin(target_channels=["sasavot"]),
    # LaughReactionBotPlugin(cooldown_seconds=30),
    # LogLaughBurstBotPlugin(laugh_markers=["hehe"]),
    # PeriodicSpamBotPlugin(messages=["Your message"], interval=DurationRange(60, 60)),
    # PyramidBotPlugin(),
    # ReactionBotPlugin(triggers=("LUL", ":)"), replies=("))", "something else")),
]

# Добавьте каналы на которые бот подключится
channels_to_connect = ["sasavot"]
event_dispatcher = EventDispatcher(plugins)

bot = TwitchBot(
    token=TWITCH_TOKEN_AOTH,
    channels_to_connect=channels_to_connect,
    twitch_secret_key=TWITCH_SECRET_KEY,
    event_dispatcher=event_dispatcher,
)

if __name__ == "__main__":
    bot.run()
