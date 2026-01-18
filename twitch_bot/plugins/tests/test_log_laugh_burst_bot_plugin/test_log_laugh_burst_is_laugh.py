import unittest

from twitch_bot.plugins.log_laugh_burst_bot_plugin import LogLaughBurstBotPlugin


class TestLogLaughBurstBotPluginIsLaugh(unittest.TestCase):

    def setUp(self) -> None:
        self.plugin = LogLaughBurstBotPlugin(laugh_markers=("marker1", "marker2"))

    def test__text_contains_laugh_marker__return_true(self) -> None:
        result = self.plugin._is_laugh("this is marker1 message")

        self.assertTrue(result)

    def test__text_without_laugh_marker__return_false(self) -> None:
        text_without_laugh_marker = "text without laugh marker"

        result = self.plugin._is_laugh(text_without_laugh_marker)

        self.assertFalse(result)

    def test__text_contains_multiply_laugh_markers__return_true(self) -> None:
        result = self.plugin._is_laugh("marker1 marker2")

        self.assertTrue(result)
