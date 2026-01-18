import unittest

from twitch_bot.plugins.pyramid_bot_plugin import PyramidBotPlugin


class TestPyramidBotPluginBuildPyramid(unittest.TestCase):

    def setUp(self):
        self.plugin: PyramidBotPlugin = PyramidBotPlugin()
        self.default_smile = self.plugin.DEFAULT_PYRAMID_SMILE

    def test__build_pyramid_height__pyramid_correct(self):
        pyramid = self.plugin._build_pyramid(1)

        self.assertEqual(
            pyramid,
            [
                self.default_smile,
            ],
        )

    def test__build_pyramid_height_2__pyramid_correct(self):
        pyramid = self.plugin._build_pyramid(2)

        self.assertEqual(
            pyramid,
            [
                self.default_smile,
                f"{self.default_smile} {self.default_smile}",
                self.default_smile,
            ],
        )

    def test__build_pyramid_length_for_all_valid_heights__pyramid_length_correct(
        self,
    ):
        for height in range(
            self.plugin.MINIMUM_PYRAMID_HEIGHT,
            self.plugin.MAXIMUM_PYRAMID_HEIGHT + 1,
        ):
            with self.subTest(height=height):
                pyramid = self.plugin._build_pyramid(height)

                self.assertEqual(
                    len(pyramid),
                    height * 2 - 1,
                    msg=f"Invalid pyramid length for height={height}",
                )
