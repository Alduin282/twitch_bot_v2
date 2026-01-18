import unittest
from twitch_bot.plugins.pyramid_bot_plugin import PyramidBotPlugin


class TestPyramidBotPluginValidateCommand(unittest.TestCase):

    def setUp(self):
        self.plugin: PyramidBotPlugin = PyramidBotPlugin()

    def test__no_height_provided__invalid(self):
        no_height_command = "pyramid"

        ok, problem_message = self.plugin._validate_pyramid_command(no_height_command)

        self.assertFalse(ok)
        self.assertEqual(problem_message, self.plugin.NO_PYRAMID_HEIGHT_MESSAGE)

    def test__height_not_number__invalid(self):
        height_not_number_command = "pyramid abs"

        ok, problem_message = self.plugin._validate_pyramid_command(
            height_not_number_command
        )

        self.assertFalse(ok)
        self.assertEqual(
            problem_message, self.plugin.PYRAMID_HEIGHT_IS_NOT_NUMBER_MESSAGE
        )

    def test__height_less_than_minimum__invalid(self):
        height_less_then_minimum_command = (
            f"pyramid {self.plugin.MINIMUM_PYRAMID_HEIGHT - 1}"
        )

        ok, problem_message = self.plugin._validate_pyramid_command(
            height_less_then_minimum_command
        )

        self.assertFalse(ok)
        self.assertEqual(
            problem_message, self.plugin.PYRAMID_HEIGHT_LESS_MINIMUM_MESSAGE
        )

    def test__height_more_than_maximum__invalid(self):
        height_more_then_maximum_command = (
            f"pyramid {self.plugin.MAXIMUM_PYRAMID_HEIGHT + 1}"
        )

        ok, problem_message = self.plugin._validate_pyramid_command(
            height_more_then_maximum_command
        )

        self.assertFalse(ok)
        self.assertEqual(
            problem_message, self.plugin.PYRAMID_HEIGHT_MORE_MAXIMUM_MESSAGE
        )

    def test__valid_height__valid(self):
        valid_command = "pyramid 5"

        ok, problem_message = self.plugin._validate_pyramid_command(valid_command)

        self.assertTrue(ok)
        self.assertEqual(problem_message, "")

    def test__valid_command_with_third_argument__ignore_third_argument(self):
        third_argument = "third_argument"
        command_with_third_argument = f"pyramid 3 {third_argument}"

        ok, problem_message = self.plugin._validate_pyramid_command(
            command_with_third_argument
        )

        self.assertTrue(ok)
        self.assertEqual(problem_message, "")
