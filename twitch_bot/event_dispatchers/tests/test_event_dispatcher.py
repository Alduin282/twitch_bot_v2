import asyncio
from typing import Awaitable
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch

from twitch_bot.event_dispatchers.event_dispatcher import EventDispatcher
from twitch_bot.definitions import EventType


class TestEventDispatcherInit(IsolatedAsyncioTestCase):

    def test__init__collects_event_handlers_from_plugins(self) -> None:
        handler_1 = AsyncMock()
        handler_2 = AsyncMock()

        test_event_type = EventType.READY
        plugin_1 = self._get_plugin_mock(test_event_type, handler_1)
        plugin_2 = self._get_plugin_mock(test_event_type, handler_2)

        dispatcher = EventDispatcher([plugin_1, plugin_2])
        result_handlers = dispatcher._event_handlers[test_event_type]

        expected_handlers = [handler_1, handler_2]
        self.assertEqual(result_handlers, expected_handlers)

    async def test__dispatch__calls_handlers_by_event_type(self) -> None:
        handler_1 = AsyncMock()
        handler_2 = AsyncMock()

        event_type_to_dispatch = EventType.READY
        plugin = MagicMock()
        plugin.get_event_handlers.return_value = {
            event_type_to_dispatch: handler_1,
            EventType.MESSAGE: handler_2,
        }
        handler_arg = "bot"
        dispatcher = EventDispatcher([plugin])

        await dispatcher.dispatch(event_type_to_dispatch, handler_arg)

        handler_1.assert_awaited_once_with(handler_arg)
        handler_2.assert_not_called()

    async def test__dispatch__no_handlers__does_nothing(self) -> None:
        dispatcher = EventDispatcher([])

        # не должно упасть
        await dispatcher.dispatch(EventType.READY, "handler_arg")

    async def test__dispatch__exception_in_one_handler__does_not_stop_others(
        self,
    ) -> None:
        failing_handler = AsyncMock(side_effect=RuntimeError("boom"))
        ok_handler = AsyncMock()
        test_event_type = EventType.READY

        failing_plugin = self._get_plugin_mock(test_event_type, failing_handler)
        ok_plugin = self._get_plugin_mock(test_event_type, ok_handler)

        dispatcher = EventDispatcher([failing_plugin, ok_plugin])

        await dispatcher.dispatch(test_event_type, "handler_arg")

        failing_handler.assert_awaited_once()
        ok_handler.assert_awaited_once()

    async def test__safe_call__logs_exception(self) -> None:
        handler = AsyncMock(side_effect=ValueError("fail"))
        test_event_type = EventType.READY
        plugin = self._get_plugin_mock(test_event_type, handler)

        dispatcher = EventDispatcher([plugin])

        with patch(
            "twitch_bot.event_dispatchers.event_dispatcher.logger.exception"
        ) as log_mock:
            await dispatcher.dispatch(test_event_type, "bot")

        log_mock.assert_called_once()

        _, kwargs = log_mock.call_args
        extra = kwargs["extra"]

        self.assertEqual(extra["event"], test_event_type.value)

    async def test__dispatch__asyncio_gather_for_parallel_execution(self) -> None:
        handler_1 = AsyncMock()
        handler_2 = AsyncMock()

        test_event_type = EventType.READY
        plugin_1 = self._get_plugin_mock(test_event_type, handler_1)
        plugin_2 = self._get_plugin_mock(test_event_type, handler_2)

        dispatcher = EventDispatcher([plugin_1, plugin_2])

        with patch(
            "twitch_bot.event_dispatchers.event_dispatcher.asyncio.gather",
            wraps=asyncio.gather,
        ) as gather_mock:
            await dispatcher.dispatch(EventType.READY, "bot")

        gather_mock.assert_called_once()
        handler_1.assert_awaited_once()
        handler_2.assert_awaited_once()

    def test__get_plugin_name__method_handler(self) -> None:
        class TestPlugin:
            async def handler(self): ...

        plugin = TestPlugin()
        dispatcher = EventDispatcher([])

        name = dispatcher._get_plugin_name(plugin.handler)

        self.assertEqual(name, "TestPlugin")

    @staticmethod
    def _get_plugin_mock(even_type: EventType, handler: Awaitable) -> MagicMock:
        plugin = MagicMock()
        plugin.get_event_handlers.return_value = {even_type: handler}
        return plugin
