import unittest
from unittest.mock import AsyncMock, patch

from twitch_bot.plugins.helpers import DurationRange, sleep_in_range


class TestSleepInRange(unittest.IsolatedAsyncioTestCase):

    @patch("twitch_bot.plugins.helpers.asyncio.sleep", new_callable=AsyncMock)
    async def test__max_seconds_zero__does_not_sleep(self, mock_sleep: AsyncMock):
        duration_range = DurationRange(
            min_seconds=0.0,
            max_seconds=0.0,
        )

        await sleep_in_range(duration_range)

        mock_sleep.assert_not_called()

    @patch("twitch_bot.plugins.helpers.random.uniform", return_value=0.42)
    @patch("twitch_bot.plugins.helpers.asyncio.sleep", new_callable=AsyncMock)
    async def test__positive_max_seconds__sleeps_with_random_duration(
        self, mock_sleep: AsyncMock, mock_random_uniform: AsyncMock
    ):
        duration_range = DurationRange(
            min_seconds=0.1,
            max_seconds=1.0,
        )

        await sleep_in_range(duration_range)

        mock_random_uniform.assert_called_once_with(
            duration_range.min_seconds,
            duration_range.max_seconds,
        )
        mock_sleep.assert_awaited_once_with(0.42)
