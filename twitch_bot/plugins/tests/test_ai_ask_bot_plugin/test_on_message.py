import unittest
from unittest.mock import AsyncMock, MagicMock
from twitchio import Channel
from twitch_bot.plugins.ai_ask_bot_plugin import AIAskPlugin


class TestAIAskPluginOnMessage(unittest.IsolatedAsyncioTestCase):

    async def test__message_without_ask_command__ignored(self) -> None:
        ai_service = self._get_ai_service_mock()
        plugin = AIAskPlugin(ai_service=ai_service)

        channel = self._get_channel_mock("test_channel")
        message_without_ask = self._get_message_mock(
            "message_without_ask_command", channel
        )

        await plugin._on_message(MagicMock(), message_without_ask)

        channel.send.assert_not_called()
        ai_service.answer.assert_not_called()

    async def test__cooldown_not_ready__does_nothing(self) -> None:
        ai_service = self._get_ai_service_mock()
        plugin = AIAskPlugin(
            ai_service=ai_service,
            cooldown_seconds=9999,
        )

        channel = self._get_channel_mock("test_channel")
        message = self._get_message_mock(
            f"{plugin.COMMAND} something",
            channel,
        )

        await plugin._on_message(MagicMock(), message)  # тригер кулдаун
        await plugin._on_message(MagicMock(), message)

        channel.send.assert_awaited_once()
        ai_service.answer.assert_awaited_once()

    async def test__ask_without_question__sends_help_message(self) -> None:
        ai_service = self._get_ai_service_mock()
        plugin = AIAskPlugin(ai_service=ai_service)

        channel = self._get_channel_mock("test_channel")
        ask_without_question_message = self._get_message_mock(
            f"{plugin.COMMAND} ", channel
        )

        await plugin._on_message(MagicMock(), ask_without_question_message)

        channel.send.assert_awaited_once_with(plugin.NO_QUESTION_ANSWER)
        ai_service.answer.assert_not_called()

    async def test__valid_question__calls_ai_and_sends_answer(self) -> None:
        ai_answer = "some ai answer"
        ai_service = self._get_ai_service_mock(answer=ai_answer)
        plugin = AIAskPlugin(ai_service=ai_service)

        channel = self._get_channel_mock("test_channel")
        user_question = "some question?"
        message = self._get_message_mock(f"{plugin.COMMAND} {user_question}", channel)

        await plugin._on_message(MagicMock(), message)

        ai_service.answer.assert_awaited_once_with(user_question)
        channel.send.assert_awaited_once_with(ai_answer)

    async def test__long_ai_answer__is_trimmed_to_500_chars(self) -> None:
        long_answer = "a" * 1000
        ai_service = self._get_ai_service_mock(answer=long_answer)
        plugin = AIAskPlugin(ai_service=ai_service)

        channel = self._get_channel_mock("test_channel")
        message = self._get_message_mock(f"{plugin.COMMAND} some question?", channel)

        await plugin._on_message(MagicMock(), message)

        long_answer_trimmed = long_answer[:500]
        channel.send.assert_awaited_once_with(long_answer_trimmed)

    @staticmethod
    def _get_channel_mock(channel_name: str) -> MagicMock:
        channel = AsyncMock()
        channel.name = channel_name
        return channel

    @staticmethod
    def _get_message_mock(content: str, channel: Channel) -> MagicMock:
        message = MagicMock()
        message.content = content
        message.channel = channel
        return message

    @staticmethod
    def _get_ai_service_mock(answer: str = "some ai answer") -> MagicMock:
        ai_service = AsyncMock()
        ai_service.answer.return_value = answer
        return ai_service
