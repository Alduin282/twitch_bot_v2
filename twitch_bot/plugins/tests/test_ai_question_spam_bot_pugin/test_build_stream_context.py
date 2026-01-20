from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock
from twitch_bot.plugins.ai_question_spam_bot_plugin import AIQuestionSpamPlugin
from twitch_bot.plugins.helpers import DurationRange


class TestAIQuestionSpamBuildStreamContext(IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.plugin = AIQuestionSpamPlugin(
            ai_service=MagicMock(),
            interval=DurationRange(1, 2),
        )

    def test__no_stream__empty_context(self) -> None:
        result = self.plugin._build_stream_context(stream=None)
        self.assertEqual(result, "")

    def test__stream_with_all_fields_for_context__add_all_fields_in_context(
        self,
    ) -> None:
        tag1 = "tag1"
        tag2 = "teg2"
        game_name = "test_game_name"
        stream_title = "test_title"

        stream = self._get_stream_mock(
            title=stream_title, game_name=game_name, tags=[tag1, tag2]
        )

        result = self.plugin._build_stream_context(stream)

        self.assertIn(stream_title, result)
        self.assertIn(game_name, result)
        self.assertIn(f"{tag1}, {tag2}", result)

    def test__stream_without_tags__default_field_in_result(self) -> None:
        stream = self._get_stream_mock(tags=[])

        result = self.plugin._build_stream_context(stream)

        self.assertIn(self.plugin.NO_TAGS, result)

    def test__stream_without_title__default_field_in_result(self) -> None:
        stream = self._get_stream_mock(title=None)

        result = self.plugin._build_stream_context(stream)

        self.assertIn(self.plugin.NO_TITLE, result)

    def test__stream_without_game__default_field_in_result(self) -> None:
        stream = self._get_stream_mock(game_name=None)

        result = self.plugin._build_stream_context(stream)

        self.assertIn(self.plugin.NO_GAME_NAME, result)

    @staticmethod
    def _get_stream_mock(
        title: str | None = "test_stream_title",
        game_name: str | None = "test_game_name",
        tags: list[str] = ["tag1", "tag2"],
    ) -> MagicMock:
        stream = MagicMock()
        stream.title = title
        stream.game_name = game_name
        stream.tags = tags
        return stream
