import asyncio
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch
from twitch_bot.plugins.console_chat_bot_plugin import ConsoleChatBotPlugin


class TestConsoleChatBotOnReady(IsolatedAsyncioTestCase):

    async def test__on_ready__creates_background_task(self) -> None:
        plugin = ConsoleChatBotPlugin()
        bot = MagicMock()

        with patch("asyncio.create_task") as create_task_mock:
            await plugin._on_ready(bot)

        create_task_mock.assert_called_once()
        task_coroutine = create_task_mock.call_args.args[0]
        self.assertTrue(asyncio.iscoroutine(task_coroutine))
