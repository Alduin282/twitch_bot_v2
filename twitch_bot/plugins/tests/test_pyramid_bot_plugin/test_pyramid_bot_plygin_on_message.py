import unittest
from unittest.mock import AsyncMock, MagicMock

from twitch_bot.plugins.pyramid_bot_plugin import PyramidBotPlugin
from twitch_bot.twitch_bot import TwitchBot


class TestPyramidBotPluginOnMessage(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        self.plugin: PyramidBotPlugin = PyramidBotPlugin()
        self.default_smile = self.plugin.DEFAULT_PYRAMID_SMILE
        self.command = self.plugin.COMMAND

        self.bot: MagicMock = MagicMock(spec=TwitchBot)

        self.author = "test_user"
        self.message: MagicMock = MagicMock()
        self.message.channel.send = AsyncMock()
        self.message.author.name = self.author

    async def test__not_pyramid_command__no_action(self) -> None:
        self.message.content = "not_pyramid_command"

        await self.plugin._on_message(self.bot, self.message)

        self.message.channel.send.assert_not_called()

    async def test__invalid_command__sends_problem_message(self) -> None:
        invalid_command = f"{self.command}"
        problem_message = self.plugin.NO_PYRAMID_HEIGHT_MESSAGE
        self.message.content = invalid_command

        await self.plugin._on_message(self.bot, self.message)

        self.message.channel.send.assert_awaited_once_with(
            f"@{self.author} {problem_message}"
        )

    async def test__valid_command__sends_pyramid(self) -> None:
        valid_command = f"{self.command} 3"
        self.message.content = valid_command

        await self.plugin._on_message(self.bot, self.message)

        expected_calls = [
            (f"{self.default_smile}",),
            (f"{self.default_smile} {self.default_smile}",),
            (f"{self.default_smile} {self.default_smile} {self.default_smile}",),
            (f"{self.default_smile} {self.default_smile}",),
            (f"{self.default_smile}",),
        ]

        actual_calls = self.message.channel.send.await_args_list

        self.assertEqual(len(actual_calls), len(expected_calls))

        for actual, expected in zip(actual_calls, expected_calls):
            self.assertEqual(actual.args, expected)

    async def test__valid_command_with_smile__sends_pyramid_with_smile(self) -> None:
        smile = "smile"
        valid_command = f"{self.command} 2 {smile}"
        self.message.content = valid_command

        await self.plugin._on_message(self.bot, self.message)

        expected_calls = [
            (f"{smile}",),
            (f"{smile} {smile}",),
            (f"{smile}",),
        ]

        actual_calls = self.message.channel.send.await_args_list

        self.assertEqual(len(actual_calls), len(expected_calls))

        for actual, expected in zip(actual_calls, expected_calls):
            self.assertEqual(actual.args, expected)

    async def test__valid_command_with_extra_args__ignores_extra_args(self) -> None:
        smile = "smile"
        valid_command = f"{self.command} 2 {smile} extra_arg"
        self.message.content = valid_command

        await self.plugin._on_message(self.bot, self.message)

        expected_calls = [
            (f"{smile}",),
            (f"{smile} {smile}",),
            (f"{smile}",),
        ]

        actual_calls = self.message.channel.send.await_args_list

        self.assertEqual(len(actual_calls), len(expected_calls))

        for actual, expected in zip(actual_calls, expected_calls):
            self.assertEqual(actual.args, expected)
