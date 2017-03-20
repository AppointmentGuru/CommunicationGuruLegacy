from django.test import TestCase, override_settings
from .Sender import CommunicationClient, Templatizer
from .models import MessageTemplate
from django.core import mail
from django.conf import settings
from django.contrib.auth import get_user_model
import unittest

'''
TODO:
-----
* Split this into ./tests/...
'''

MOCK_GURU_COMMUNICATIONS = {
    'SMS_BACKEND': 'gurucommunication.backends.mocksms.MockSMSBackend',
    'PREFERENCE_ORDER': ['SMS', 'EMAIL', 'NOTIFICATION'],
    'DEFAULT_DELIVERY_METHOD': 'EMAIL'
}

class BasicSendTestCase(TestCase):

    @override_settings(GURU_COMMUNICATIONS=MOCK_GURU_COMMUNICATIONS)
    def test_send_sms(self):
        sender = CommunicationClient('SMS')
        sender.send('+27831234567', 'testing')

    def test_send_email(self):
        sender = CommunicationClient('EMAIL')
        message = {
            'message': 'test',
            'subject': 'this is a test',
            'from_string': 'Christo Crampton <info@38.co.za>',
        }
        sender.send(['christo@creativecolibri.com'], 'testing testing 1,2,3')

        assert len(mail.outbox) == 1

    def test_send_templated_email(self):
        pass

class TemplatizerBasicRenderTestCase(TestCase):

    def setUp(self):
        self.t = Templatizer()

    def test_render(self):
        test_string = "Hello **{{foo}}**."
        context = {"foo": "bar"}
        result = self.t.render(message=test_string, context=context)

        expected_result = '<html>\n\t<body>\n\t<p>Hello <strong>bar</strong>.</p>\n\n\t</body>\n</html>'
        assert expected_result == result,\
            'Expected "{}". Got: "{}"' . format (expected_result, result)

    def test_render_to_sms(self):
        test_string = "Hello {{foo}}."
        context = {"foo": "bar"}
        result = self.t.render_to_sms(message=test_string, context=context)

        expected_result = "Hello bar."
        assert result == expected_result, \
            'Expected: "{}". Got: "{}"' . format (expected_result, result)

class TemplatizerTemplateRenderTestCase(TestCase):

    def setUp(self):
        self.user1 = get_user_model().objects.create(username='joesoap', password='testtest')
        self.user2 = get_user_model().objects.create(username='joesoap', password='testtest')
        self.template_id = test_email
        data = {
            "owner": self.user1,
            "template_id": self.template_id,
            "name": "Test email",
            "subject": "Hi",
            "is_default_message": True,
            "long_message": "Hello there! {{person}}",
            "short_message": "Hello there! {{person}}",
        }
        MessageTemplate.objects.create(**data)
        self.t = Templatizer()

    def test_send_templated_email_uses_default_if_no_custom_template_defined(self):


    def test_can_overide_default_templated_email(self):
        pass





