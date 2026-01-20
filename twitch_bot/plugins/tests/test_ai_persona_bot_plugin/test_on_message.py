from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock

from twitch_bot.plugins.ai_persona_pluign import AIPersonaPlugin


class TestAIPersona(IsolatedAsyncioTestCase):

    async def test__persona_command__sends_current_persona(self) -> None:
        persona = "test persona"
        ai_service = self._get_ai_service_mock(persona)

        plugin = AIPersonaPlugin(ai_service)
        command = plugin.GET_PERSONA_COMMAND
        message_with_persona_command = self._get_message_mock(content=command)

        await plugin._on_message(MagicMock(), message_with_persona_command)

        ai_service.get_persona.assert_called_once()
        message_with_persona_command.channel.send.assert_awaited_once_with(persona)

    async def test__persona_random_not_mod__do_nothing(self) -> None:
        ai_service = self._get_ai_service_mock()
        plugin = AIPersonaPlugin(ai_service)

        command = plugin.RANDOM_PERSONA_COMMAND
        message = self._get_message_mock(command, is_mod=False)

        await plugin._on_message(MagicMock(), message)

        ai_service.set_random_persona.assert_not_called()
        message.channel.send.assert_not_awaited()

    async def test__persona_random_mod__updates_persona(self) -> None:
        ai_service = self._get_ai_service_mock()
        plugin = AIPersonaPlugin(ai_service)

        command = plugin.RANDOM_PERSONA_COMMAND
        message = self._get_message_mock(command, is_mod=True)

        await plugin._on_message(MagicMock(), message)

        ai_service.set_random_persona.assert_awaited_once()
        message.channel.send.assert_awaited_once()

    async def test__persona_reset_not_mod__do_nothing(self) -> None:
        ai_service = self._get_ai_service_mock()
        plugin = AIPersonaPlugin(ai_service)

        command = plugin.RESET_PERSONA_COMMAND
        message = self._get_message_mock(command, is_mod=False)

        await plugin._on_message(MagicMock(), message)

        ai_service.set_random_persona.assert_not_called()
        message.channel.send.assert_not_awaited()

    async def test__persona_reset_mod__resets_persona(self) -> None:
        ai_service = self._get_ai_service_mock()
        plugin = AIPersonaPlugin(ai_service)

        command = plugin.RESET_PERSONA_COMMAND
        message = self._get_message_mock(command, is_mod=True)

        await plugin._on_message(MagicMock(), message)

        ai_service.reset_persona.assert_called_once()
        message.channel.send.assert_awaited_once()

    async def test__unknown_command__do_nothing(self) -> None:
        ai_service = self._get_ai_service_mock()
        plugin = AIPersonaPlugin(ai_service)

        message = self._get_message_mock("!persona unknown_command")

        await plugin._on_message(MagicMock(), message)

        message.channel.send.assert_not_awaited()

    @staticmethod
    def _get_ai_service_mock(persona: str = "test_persona") -> MagicMock:
        ai_service = MagicMock()
        ai_service.get_persona.return_value = persona
        ai_service.set_random_persona = AsyncMock()
        return ai_service

    @staticmethod
    def _get_channel_mock():
        channel = AsyncMock()
        return channel

    def _get_message_mock(
        self,
        content: str,
        is_mod: bool = False,
    ):
        message = MagicMock()
        message.content = content
        message.channel = self._get_channel_mock()

        author = MagicMock()
        author.is_mod = is_mod
        message.author = author

        return message
