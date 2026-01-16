from unittest.mock import MagicMock
from twitch_bot.plugins.tests.test_reaction_bot_plugin.test_reaction_bot_base import (
    ReactionPluginTestBase,
)
from twitchio import Message, Channel, User


class TestReactionBotPluginShouldReact(ReactionPluginTestBase):
    def setUp(self) -> None:
        pass

    def test__trigger_in_content__should_react(self):
        test_triggers = ("trigger",)
        test_replies = ("reply",)
        message_with_trigger = self._make_message(test_triggers[0])
        reaction_plugin = self.create_reaction_plugin(test_triggers, test_replies)

        result = reaction_plugin._should_react(
            reaction_plugin.reaction_rule, message_with_trigger
        )
        self.assertTrue(result)

    def test__trigger_not_in_content__should_not_react(self):
        test_triggers = ("trigger",)
        test_replies = ("reply",)
        message_without_trigger = self._make_message("message_without_trigger")
        reaction_plugin = self.create_reaction_plugin(test_triggers, test_replies)

        result = reaction_plugin._should_react(
            reaction_plugin.reaction_rule, message_without_trigger
        )
        self.assertFalse(result)

    def test__echo_and_ignore_echo__should_not_react(self):
        reaction_plugin = self.create_reaction_plugin(ignore_echo=True)
        echo_message_with_trigger = self._make_message(
            reaction_plugin.reaction_rule.triggers[0], echo=True
        )

        result = reaction_plugin._should_react(
            reaction_plugin.reaction_rule, echo_message_with_trigger
        )
        self.assertFalse(result)

    def test__echo_but_ignore_echo_false__should_react(self):
        reaction_plugin = self.create_reaction_plugin(ignore_echo=False)
        echo_message_with_trigger = self._make_message(
            reaction_plugin.reaction_rule.triggers[0], echo=True
        )

        result = reaction_plugin._should_react(
            reaction_plugin.reaction_rule, echo_message_with_trigger
        )
        self.assertTrue(result)

    def test__probability_0__should_not_react(self):
        reaction_plugin = self.create_reaction_plugin(reaction_probability=0)
        message_with_trigger = self._make_message(
            reaction_plugin.reaction_rule.triggers[0]
        )

        result = reaction_plugin._should_react(
            reaction_plugin.reaction_rule, message_with_trigger
        )
        self.assertFalse(result)

    def test__probability_1__should_react(self):
        reaction_plugin = self.create_reaction_plugin(reaction_probability=1)
        message_with_trigger = self._make_message(
            reaction_plugin.reaction_rule.triggers[0]
        )

        result = reaction_plugin._should_react(
            reaction_plugin.reaction_rule, message_with_trigger
        )
        self.assertTrue(result)

    def test__upper_case_trigger_lower_case_content__should_not_react(self):
        upper_case_trigger = "TRIGGER"
        triggers = (upper_case_trigger,)
        lower_case_message_content = self._make_message(upper_case_trigger.lower())
        reaction_plugin = self.create_reaction_plugin(triggers)

        result = reaction_plugin._should_react(
            reaction_plugin.reaction_rule, lower_case_message_content
        )
        self.assertFalse(result)

    def test__partial_trigger_not_matched__should_not_react(self):
        triggers = ("trigger",)
        partial_trigger = "trigger!"
        message_content_with_partial_trigger = self._make_message(partial_trigger)
        reaction_plugin = self.create_reaction_plugin(triggers)

        result = reaction_plugin._should_react(
            reaction_plugin.reaction_rule, message_content_with_partial_trigger
        )
        self.assertFalse(result)

    def test__multiply_words_content_with_trigger__should_react(self):
        triggers = ("trigger",)
        content = "not_trigger trigger"
        message_with_trigger = self._make_message(content)
        reaction_plugin = self.create_reaction_plugin(triggers)

        result = reaction_plugin._should_react(
            reaction_plugin.reaction_rule, message_with_trigger
        )
        self.assertTrue(result)

    def _make_message(self, content: str, echo: bool = False) -> Message:
        mock_channel = MagicMock(spec=Channel)
        mock_channel.name = "test_channel"
        mock_user = MagicMock(spec=User)
        mock_user.name = "viewer"
        return Message(
            content=content,
            author=mock_user,
            channel=mock_channel,
            id="1",
            echo=echo,
            tags={},
        )
