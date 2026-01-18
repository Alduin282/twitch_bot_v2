import unittest
from unittest.mock import patch

from twitch_bot.plugins.helpers import Cooldown


class TestCooldown(unittest.TestCase):

    def test__new_cooldown__is_ready(self) -> None:
        cooldown_duration = 10.0
        current_time = 100.0

        cooldown = Cooldown(duration_seconds=cooldown_duration)

        with patch("twitch_bot.plugins.helpers.time.time", return_value=current_time):
            self.assertTrue(cooldown.is_ready())

    def test__trigger__cooldown_not_ready_immediately_after(self) -> None:
        cooldown_duration = 10.0
        trigger_time = 100.0
        time_in_cooldown_window = 105.0

        cooldown = Cooldown(duration_seconds=cooldown_duration)
        with patch("twitch_bot.plugins.helpers.time.time", return_value=trigger_time):
            cooldown.trigger()

        with patch(
            "twitch_bot.plugins.helpers.time.time", return_value=time_in_cooldown_window
        ):
            self.assertFalse(cooldown.is_ready())

    def test__duration_passed_after_trigger__cooldown_is_ready(self) -> None:
        cooldown_duration = 10.0
        trigger_time = 100.0
        time_after_cooldown_window = 110.0

        cooldown = Cooldown(duration_seconds=cooldown_duration)
        with patch("twitch_bot.plugins.helpers.time.time", return_value=trigger_time):
            cooldown.trigger()

        with patch(
            "twitch_bot.plugins.helpers.time.time",
            return_value=time_after_cooldown_window,
        ):
            self.assertTrue(cooldown.is_ready())

    def test__trigger__updates_last_trigger_time(self) -> None:
        cooldown_duration = 10.0
        trigger_time = 123.456

        cooldown = Cooldown(duration_seconds=cooldown_duration)
        with patch("twitch_bot.plugins.helpers.time.time", return_value=trigger_time):
            cooldown.trigger()

        self.assertEqual(cooldown._last_trigger_time, trigger_time)

    def test__zero_duration__always_ready(self) -> None:
        cooldown_duration = 0.0
        trigger_time = 100.0

        cooldown = Cooldown(duration_seconds=cooldown_duration)
        with patch("twitch_bot.plugins.helpers.time.time", return_value=trigger_time):
            cooldown.trigger()

        with patch("twitch_bot.plugins.helpers.time.time", return_value=trigger_time):
            self.assertTrue(cooldown.is_ready())
