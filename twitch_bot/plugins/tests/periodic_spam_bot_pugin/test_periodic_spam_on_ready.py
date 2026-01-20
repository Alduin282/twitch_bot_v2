import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from twitch_bot.plugins.periodic_spam_bot_plugin import PeriodicSpamBotPlugin
from twitch_bot.plugins.helpers import DurationRange


class TestPeriodicSpamBotPluginOnReady(unittest.IsolatedAsyncioTestCase):

    async def test__delay_configured__sleeps_before_start(self):
        delay_before_start = 3.0
        plugin = PeriodicSpamBotPlugin(
            messages=["test_message"],
            interval=DurationRange(1.0, 2.0),
            delay_start_seconds=delay_before_start,
        )

        bot = MagicMock()
        bot.connected_channels = []

        with patch("asyncio.sleep", new_callable=AsyncMock) as sleep_mock:
            await plugin._on_ready(bot)

            sleep_mock.assert_awaited_once_with(delay_before_start)

    async def test__no_connected_channels__logs_warning_and_returns(self):
        plugin = PeriodicSpamBotPlugin(
            messages=["test_message"],
            interval=DurationRange(1.0, 2.0),
        )

        bot = MagicMock()
        bot.connected_channels = []

        with patch(
            "twitch_bot.plugins.periodic_spam_bot_plugin.sleep_in_range",
            new_callable=AsyncMock,
        ) as sleep_mock, patch(
            "twitch_bot.plugins.periodic_spam_bot_plugin.logger.warning"
        ) as warning_mock:
            await plugin._on_ready(bot)

            sleep_mock.assert_not_called()
            warning_mock.assert_called_once_with(
                "[PeriodicSpamBotPlugin]: no connected channels, skipping spam"
            )

    async def test__multiple_channels__sends_message_to_all_channels(self):
        message_to_send = "message_to_send"
        plugin = PeriodicSpamBotPlugin(
            messages=[message_to_send],
            interval=DurationRange(1.0, 2.0),
        )

        channel_1 = AsyncMock()
        channel_2 = AsyncMock()

        bot = MagicMock()
        bot.connected_channels = [channel_1, channel_2]

        with patch(
            "twitch_bot.plugins.periodic_spam_bot_plugin.sleep_in_range",
            new_callable=AsyncMock,
        ) as sleep_mock:
            sleep_mock.side_effect = [
                None,  # 1-я итерация
                asyncio.CancelledError,  # стоп
            ]

            with self.assertRaises(asyncio.CancelledError):
                await plugin._on_ready(bot)

            channel_1.send.assert_awaited_once_with(message_to_send)
            channel_2.send.assert_awaited_once_with(message_to_send)

    async def test__single_channel__sends_two_messages_in_two_iterations(self):
        message_to_send = "message_to_send"
        plugin = PeriodicSpamBotPlugin(
            messages=[message_to_send],
            interval=DurationRange(1.0, 2.0),
        )

        channel = AsyncMock()

        bot = MagicMock()
        bot.connected_channels = [channel]

        with patch(
            "twitch_bot.plugins.periodic_spam_bot_plugin.sleep_in_range",
            new_callable=AsyncMock,
        ) as sleep_mock:
            sleep_mock.side_effect = [
                None,  # 1-я итерация
                None,  # 2-я итерация
                asyncio.CancelledError,  # стоп
            ]

            with self.assertRaises(asyncio.CancelledError):
                await plugin._on_ready(bot)

        self.assertEqual(channel.send.await_count, 2)
        channel.send.assert_any_await(message_to_send)
        channel.send.assert_any_await(message_to_send)

    async def test__multiple_messages__random_one_sended(self) -> None:
        random_message = "random_test_message"
        multiple_messages = ["test_message", random_message]
        plugin = PeriodicSpamBotPlugin(
            messages=multiple_messages,
            interval=DurationRange(1.0, 2.0),
        )

        channel = AsyncMock()

        bot = MagicMock()
        bot.connected_channels = [channel]

        with patch(
            "twitch_bot.plugins.periodic_spam_bot_plugin.sleep_in_range",
            new_callable=AsyncMock,
        ) as sleep_mock, patch(
            "twitch_bot.plugins.periodic_spam_bot_plugin.random.choice",
            return_value=random_message,
        ) as random_choice_mock:
            sleep_mock.side_effect = [
                None,  # 1-я итерация
                asyncio.CancelledError,  # стоп
            ]

            with self.assertRaises(asyncio.CancelledError):
                await plugin._on_ready(bot)

        random_choice_mock.assert_called_once_with(multiple_messages)
        channel.send.assert_any_await(random_message)
