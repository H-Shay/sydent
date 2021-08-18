import os.path
from unittest.mock import patch

from twisted.trial import unittest

from sydent.util.emailutils import sendEmail
from tests.utils import make_sydent, make_request

import urllib


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


    def test_jinja_vector_invite(self):
        substitutions = {
                "address": "foo@example.com",
                "medium": "email",
                "room_alias": "#somewhere:exmaple.org",
                "room_avatar_url": "mxc://example.org/s0meM3dia",
                "room_id": "!something:example.org",
                "room_name": "Bob's Emporium of Messages",
                "sender": "@bob:example.com",
                "sender_avatar_url": "mxc://example.org/an0th3rM3dia",
                "sender_display_name": "<Bob Smith>",
                "bracketed_verified_sender" : "Bob Smith",
                "bracketed_room_name": "Bob's Emporium of Messages",
                "web_client_location" : "element",
                "to" : "person@test.test",
                "token": "a_token",
                "ephemeral_private_key" : "mystery_key",
                "web_client_location" : "https://app.element.io"
            }

        templateFile = self.sydent.get_branded_template(
            "vector-im",
            "invite_template.eml",
            ("email", "email.invite_template"),
        )

        with patch("sydent.util.emailutils.smtplib") as smtplib:
            sendEmail(self.sydent, templateFile, 'test@test.com', substitutions)

        smtp = smtplib.SMTP.return_value
        email_contents = smtp.sendmail.call_args[0][2].decode("utf-8")

        # test url input is encoded
        self.assertIn(urllib.parse.quote("mxc://example.org/s0meM3dia"), email_contents)

        # test html input is escaped
        self.assertIn("Bob&#39;s Emporium of Messages", email_contents)

        # test safe values are not escaped
        self.assertIn("<Bob Smith>", email_contents)

        #test our link is as expected
        expected_url = 'https://app.element.io/#/room/'+urllib.parse.quote('!something:example.org')+'?email='+urllib.parse.quote('test@test.com')+'&signurl=https%3A%2F%2Fvector.im%2F_matrix%2Fidentity%2Fapi%2Fv1%2Fsign-ed25519%3Ftoken%3D'+urllib.parse.quote('a_token')+'%26private_key%3D'+urllib.parse.quote('mystery_key')+'&room_name='+urllib.parse.quote("Bob's Emporium of Messages")+'&room_avatar_url='+urllib.parse.quote('mxc://example.org/s0meM3dia')+'&inviter_name='+urllib.parse.quote('<Bob Smith>')+'&guest_access_token=&guest_user_id='
        text = email_contents.splitlines()
        link = text[19]
        self.assertEqual(link, expected_url)

    def test_jinja_matrix_invite(self):
        substitutions = {
                "address": "foo@example.com",
                "medium": "email",
                "room_alias": "#somewhere:exmaple.org",
                "room_avatar_url": "mxc://example.org/s0meM3dia",
                "room_id": "!something:example.org",
                "room_name": "Bob's Emporium of Messages",
                "sender": "@bob:example.com",
                "sender_avatar_url": "mxc://example.org/an0th3rM3dia",
                "sender_display_name": "<Bob Smith>",
                "bracketed_verified_sender" : "Bob Smith",
                "bracketed_room_name": "Bob's Emporium of Messages",
                "web_client_location" : "element",
                "to" : "person@test.test",
                "token": "a_token",
                "ephemeral_private_key" : "mystery_key",
                "web_client_location" : "https://matrix.org"
            }

        templateFile = self.sydent.get_branded_template(
            "matrix-org",
            "invite_template.eml",
            ("email", "email.invite_template"),
        )

        with patch("sydent.util.emailutils.smtplib") as smtplib:
            sendEmail(self.sydent, templateFile, 'test@test.com', substitutions)

        smtp = smtplib.SMTP.return_value
        email_contents = smtp.sendmail.call_args[0][2].decode("utf-8")

        # test url input is encoded
        self.assertIn(urllib.parse.quote("mxc://example.org/s0meM3dia"), email_contents)

        # test html input is escaped
        self.assertIn("Bob&#39;s Emporium of Messages", email_contents)

        # test safe values are not escaped
        self.assertIn("<Bob Smith>", email_contents)

        #test our link is as expected
        expected_url = 'https://matrix.org/#/room/'+urllib.parse.quote('!something:example.org')+'?email='+urllib.parse.quote('test@test.com')+'&signurl=https%3A%2F%2Fmatrix.org%2F_matrix%2Fidentity%2Fapi%2Fv1%2Fsign-ed25519%3Ftoken%3D'+urllib.parse.quote('a_token')+'%26private_key%3D'+urllib.parse.quote('mystery_key')+'&room_name='+urllib.parse.quote("Bob's Emporium of Messages")+'&room_avatar_url='+urllib.parse.quote('mxc://example.org/s0meM3dia')+'&inviter_name='+urllib.parse.quote('<Bob Smith>')+'&guest_access_token=&guest_user_id='
        text = email_contents.splitlines()
        link = text[22]
        self.assertEqual(link, expected_url)


    def test_jinja_matrix_verification(self):
        substitutions = {
                "address": "foo@example.com",
                "medium": "email",
                "to" : "person@test.test",
                "token": "<<token>>",
                "link" : "https://link_test.com"
            }

        templateFile = self.sydent.get_branded_template(
            "matrix-org",
            "verification_template.eml",
            ("email", "email.verification_template"),
        )

        with patch("sydent.util.emailutils.smtplib") as smtplib:
            sendEmail(self.sydent, templateFile, 'test@test.com', substitutions)

        smtp = smtplib.SMTP.return_value
        email_contents = smtp.sendmail.call_args[0][2].decode("utf-8")

        # test url input is encoded
        self.assertIn(urllib.parse.quote("https://link_test.com"), email_contents)

        # test html input is escaped
        self.assertIn("&lt;&lt;token&gt;&gt;", email_contents)

        # test safe values are not escaped
        self.assertIn("<<token>>", email_contents)


    def test_jinja_vector_verification(self):
        substitutions = {
                "address": "foo@example.com",
                "medium": "email",
                "to" : "person@test.test",
                "token": "<<token>>",
                "link" : "https://link_test.com"
            }

        templateFile = self.sydent.get_branded_template(
            "vector-im",
            "verification_template.eml",
            ("email", "email.verification_template"),
        )

        with patch("sydent.util.emailutils.smtplib") as smtplib:
            sendEmail(self.sydent, templateFile, 'test@test.com', substitutions)

        smtp = smtplib.SMTP.return_value
        email_contents = smtp.sendmail.call_args[0][2].decode("utf-8")

        # test url input is encoded
        self.assertIn(urllib.parse.quote("https://link_test.com"), email_contents)

        # test all output is as expected
        path = os.path.join(self.sydent.cfg.get("general", "templates.path"), 'vector_verification_sample.txt')

        with open(path, 'r') as file:
            expected_text = file.read()

        # remove headers as they are variable
        email_contents = email_contents.splitlines()[13:]

        # remove multipart headers as they are variable
        del email_contents[40]
        del email_contents[156]
        self.assertEqual("\n".join(email_contents), expected_text)