import unittest

from twitch_bot.plugins.helpers import DurationRange


class TestDurationRangeValidation(unittest.TestCase):

    def test__valid_range__no_errors(self):
        duration: DurationRange = DurationRange(
            min_seconds=0.5,
            max_seconds=1.0,
        )

        self.assertEqual(duration.min_seconds, 0.5)
        self.assertEqual(duration.max_seconds, 1.0)

    def test__zero_min_and_max__no_errors(self):
        duration: DurationRange = DurationRange(
            min_seconds=0.0,
            max_seconds=0.0,
        )

        self.assertEqual(duration.min_seconds, 0.0)
        self.assertEqual(duration.max_seconds, 0.0)

    def test__min_greater_than_max__value_error(self):
        with self.assertRaises(ValueError):
            DurationRange(
                min_seconds=2.0,
                max_seconds=1.0,
            )

    def test__negative_min_seconds__value_error(self):
        with self.assertRaises(ValueError):
            DurationRange(
                min_seconds=-0.1,
                max_seconds=1.0,
            )

    def test__negative_max_seconds__value_error(self):
        with self.assertRaises(ValueError):
            DurationRange(
                min_seconds=0.0,
                max_seconds=-1.0,
            )

    def test__negative_min_and_max__value_error(self):
        with self.assertRaises(ValueError):
            DurationRange(
                min_seconds=-1.0,
                max_seconds=-0.5,
            )
