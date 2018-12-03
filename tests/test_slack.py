import mock
import requests
from st2tests.base import BaseActionTestCase

from lib.slack import SlackPoster, SlackNotifier


class TestSlackPoster(BaseActionTestCase):
    action_cls = SlackPoster

    @mock.patch("lib.slack.SlackNotifier", autospec=True)
    def test_successful_post(self, notifier_mock):
        action = self.get_action_instance()
        action.config["slack_webhook_url"] = "this-is-the-webhook-url"
        exit_code, out = action.run("channel", "user", "message")
        self.assertTrue(exit_code)

    @mock.patch("lib.slack.SlackNotifier", autospec=True)
    def test_unsuccessful_post(self, notifier_mock):
        action = self.get_action_instance()
        action.config["slack_webhook_url"] = "this-is-the-webhook-url"
        notifier = notifier_mock.return_value
        notifier.post_message.side_effect = requests.exceptions.HTTPError("a mock HTTPError")
        exit_code, out = action.run("channel", "user", "message")
        self.assertFalse(exit_code)
