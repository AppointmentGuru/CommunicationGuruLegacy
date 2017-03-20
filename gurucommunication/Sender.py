from django.conf import settings
from django.utils.module_loading import import_string
from django.template.loader import render_to_string
from django.core import mail
from django.template import engines

from .models import MessageTemplate

class Templatizer:

    def __parse_message(self, message, context):
        django_engine = engines['django']

        message_template = django_engine.from_string(message)
        message = message_template.render(context=context).strip()
        return message

    def __get_default_template(self, template_id):
        return MessageTemplate.objects.get(template_id=template_id, is_default_message=True)

    def get_messaage_template(self, template_id, user_id=None):

        if user_id is None:
            return self.__get_default_template(template_id)

        try:
            return MessageTemplate.objects.get(template_id=template_id, user_id=user_id)
        except MessageTemplate.DpesNotExist:
            return self.__get_default_template


    def render(self, message, context, base_template='gurucommunication/base.html'):
        message = self.__parse_message(message, context)
        message_context = {
            "message": message
        }
        return render_to_string(base_template, context=message_context).strip()

    def render_to_sms(self, message, context):
        '''
        A thin wrapper around render() which just makes sure we use a blank template (with markdown)
        '''
        return self.__parse_message(message, context)

class CommunicationClient:

    SMS_REQUIRED_FIELDS = []
    EMAIL_REQUIRED_FIELDS = []

    def __init__(self, preferred_medium):
        '''
        Given the inputs. If possible, send it to the preferred medium
        otherwise, send it to the best possible option available
        If impossible to send (no email, sms or whatever an app needs):
        mark it as failed in the log
        '''

        self.medium = preferred_medium
        if preferred_medium == settings.GURU_MEDIUMS.SMS:
            sms_backend = settings.GURU_COMMUNICATIONS.get('SMS_BACKEND')
            self.client = import_string(sms_backend)()
        if preferred_medium == settings.GURU_MEDIUMS.EMAIL:
            self.client = mail

    def send_template(self, to, template_id, user_id, context):
        '''
        Send a templated/pre-defined message
        '''
        templatizer = Templatizer()
        template = templatizer.get_messaage_template(template_id, user_id)
        message = templatizer.render(template_id, message, context)

        self.send(to, message)

    def send(self, to, message, subject=None, sender=None, **kwargs):
        '''
        base send method: sends an email
        '''
        if self.medium == settings.GURU_MEDIUMS.SMS:
            # validate input and throw errors as appropriate:
            result = self.client.send(message, to)
            # save to log
            return result

        if self.medium == settings.GURU_MEDIUMS.EMAIL:
            result = self.client.send_mail(
                subject,
                message,
                sender,
                to, html_message=message
            )
            # save to log:
            return result