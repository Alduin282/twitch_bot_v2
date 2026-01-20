from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, patch

import asyncio

from twitch_bot.ai.ai_ollama_service import AIOllamaService


class TestAIOllamaService(IsolatedAsyncioTestCase):

    async def test__answer__calls_chat_and_returns_response(self) -> None:
        ai_service = AIOllamaService()
        answer = "test answer"
        ai_service._chat = AsyncMock(return_value=answer)
        question = "test question?"

        result = await ai_service.answer(question)

        self.assertEqual(result, answer)
        ai_service._chat.assert_awaited_once()

        messages = ai_service._chat.call_args.args[0]
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[1]["role"], "user")
        self.assertEqual(messages[1]["content"], question)

    async def test__ask_streamer__builds_context_and_returns_response(self) -> None:
        ai_service = AIOllamaService()
        question = "test question ?"
        ai_service._chat = AsyncMock(return_value=question)
        stream_context = "stream context"

        result = await ai_service.ask_streamer(stream_context)

        self.assertEqual(result, question)
        ai_service._chat.assert_awaited_once()

        messages = ai_service._chat.call_args.args[0]
        user_prompt = messages[1]["content"]

        self.assertIn(stream_context, user_prompt)
        self.assertIn(ai_service.REQUEST_FOR_QUESTION, user_prompt)

    async def test__set_random_persona__updates_persona(self) -> None:
        ai_service = AIOllamaService()
        persona = "test persona"
        ai_service._chat = AsyncMock(return_value=persona)

        await ai_service.set_random_persona()

        self.assertEqual(ai_service.persona, persona)
        ai_service._chat.assert_awaited_once()

    def test__reset_persona__sets_default(self) -> None:
        ai_service = AIOllamaService()
        ai_service.persona = "test random persona"

        ai_service.reset_persona()

        self.assertEqual(ai_service.persona, ai_service.DEFAULT_PERSONA)

    def test__get_persona__returns_current_persona(self) -> None:
        ai_service = AIOllamaService()

        persona = ai_service.get_persona()

        self.assertEqual(persona, ai_service.DEFAULT_PERSONA)

    def test__build_system_prompt__contains_persona_and_base_prompt(self) -> None:
        ai_service = AIOllamaService()

        prompt = ai_service._build_system_prompt()

        self.assertIn(ai_service.persona, prompt)
        self.assertIn(ai_service.BASE_PROMPT, prompt)

    async def test__chat_timeout__returns_fallback_message(self) -> None:
        ai_service = AIOllamaService(request_timeout=1)

        with patch(
            "asyncio.wait_for",
            side_effect=asyncio.TimeoutError,
        ):
            result = await ai_service._chat([])

        self.assertEqual(ai_service.TIMEOUT_ANSWER, result)

    async def test__chat_exception__returns_error_message(self) -> None:
        ai_service = AIOllamaService()

        with patch(
            "asyncio.wait_for",
            side_effect=RuntimeError("boom"),
        ):
            result = await ai_service._chat([])

        self.assertEqual(ai_service.EXCEPTION_ANSWER, result)

    async def test__chat_success__returns_message_content(self) -> None:
        ai_service = AIOllamaService()

        ollama_content = "some test content"
        ollama_response = {"message": {"content": f"{ollama_content}"}}

        with patch(
            "asyncio.wait_for",
            return_value=ollama_response,
        ):
            result = await ai_service._chat([])

        self.assertEqual(result, ollama_content)

    async def test__chat_no_content__returns_no_content_message(self) -> None:
        ai_service = AIOllamaService()

        ollama_response = {"message": {"no_content": "really_no_content"}}

        with patch(
            "asyncio.wait_for",
            return_value=ollama_response,
        ):
            result = await ai_service._chat([])

        self.assertEqual(result, ai_service.NO_CONTENT_ANSWER)
