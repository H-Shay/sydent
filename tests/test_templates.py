import os.path
from unittest.mock import patch

from twisted.trial import unittest

from sydent.util.emailutils import sendEmail
from tests.utils import make_sydent


class TestTemplate(unittest.TestCase):
    def setUp(self):
        # Create a new sydent
        config = {
            "general": {
                "templates.path": os.path.join(
                    os.path.dirname(os.path.dirname(__file__)), "res"
                ),
            },
        }
        self.sydent = make_sydent(test_config=config)

    def test_jinja_template(self):
        # test matrix invite template
        templateFile = self.sydent.get_branded_template(
            "matrix", "invite_template.eml.j2", ("email", "email.invite_template")
        )
        substitutions = {"sender_display_name": "Betty Boop"}

        with patch("sydent.util.emailutils.smtplib") as smtplib:
            sendEmail(self.sydent, templateFile, "blah@nowhere.com", substitutions)

        smtp = smtplib.SMTP.return_value
        email_contents = smtp.sendmail.call_args[0][2].decode("utf-8")

        self.assertIn("Betty Boop", email_contents)

        # test vector-im verification template
        templateFile = self.sydent.get_branded_template(
            "vector-im",
            "verification_template.eml.j2",
            ("email", "email.verification_template"),
        )
        substitutions = {}

        with patch("sydent.util.emailutils.smtplib") as smtplib:
            sendEmail(self.sydent, templateFile, "mickey@mouse.org", substitutions)

        smtp = smtplib.SMTP.return_value
        email_contents = smtp.sendmail.call_args[0][2].decode("utf-8")

        self.assertIn("mickey@mouse.org", email_contents)

    def test_jinja_escapes_invite(self):
        templateFile = self.sydent.get_branded_template(
            "matrix", "invite_template.eml.j2", ("email", "email.invite_template")
        )
        substitutions = {"sender_display_name_forhtml": "<malicious html>"}

        with patch("sydent.util.emailutils.smtplib") as smtplib:
            sendEmail(self.sydent, templateFile, "blah@nowhere.com", substitutions)

        smtp = smtplib.SMTP.return_value
        email_contents = smtp.sendmail.call_args[0][2].decode("utf-8")
        self.assertNotIn("<malicious html>", email_contents)

    def test_jinja_does_not_escape_safe_values(self):
        templateFile = self.sydent.get_branded_template(
            "vector-im",
            "verification_template.eml.j2",
            ("email", "email.verification_template"),
        )
        substitutions = {"link": "<i'm html>"}

        with patch("sydent.util.emailutils.smtplib") as smtplib:
            sendEmail(self.sydent, templateFile, "blah@nowhere.com", substitutions)

        smtp = smtplib.SMTP.return_value
        email_contents = smtp.sendmail.call_args[0][2].decode("utf-8")
        self.assertIn("<i'm html>", email_contents)