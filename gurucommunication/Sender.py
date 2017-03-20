from django.conf import settings
from django.utils.module_loading import import_string
from django.template.loader import render_to_string
from django.core import mail
from django.template import engines

from .models import MessageTemplate

class Sender:
    phone=None
    email=None
    app_id=None
    name=None

    @classmethod
    def from_user(cls, user):
        person = cls()
        person.phone = user.profile.phone # make this dynamic / a setting
        person.email = user.email
        person.app_id = user.username # make this dyamic / a setting
        person.name = user.get_full_name()
        return person

class Recipient:
    phone=None
    email=None
    app_id=None
    name=None

    @classmethod
    def from_user(cls, user):
        person = cls()
        person.phone = user.profile.phone # make this dynamic / a setting
        person.email = user.email
        person.app_id = user.username # make this dyamic / a setting
        person.name = user.get_full_name()
        return person

# work in progress. This will become the preferred way to send messages:
def send_template(to, template_id, context, template_owner):
    '''
    usage:

    send_template(
        to=Recipient.from_user(user),
        from=Sender.from_user(sender_user),
        template_id='hello-world',
        context={},
        template_owner=user)
    '''
    msg = self.t.get_message_template(template_id)
    return CommunicationClient(msg.preferred_delivery_method).send_template(
        to=to,
        template_id=self.template_id,
        context=context,
        owner=template_owner
    )

class Templatizer:

    def __parse_message(self, message, context):
        django_engine = engines['django']

        message_template = django_engine.from_string(message)
        message = message_template.render(context=context).strip()
        return message

    def __get_default_template(self, template_id):
        return MessageTemplate.objects.get(template_id=template_id, is_default_template=True)

    def get_message_template(self, template_id, user_id=None):

        if user_id is None:
            return self.__get_default_template(template_id)

        try:
            return MessageTemplate.objects.get(template_id=template_id, owner_id=user_id)
        except MessageTemplate.DoesNotExist:
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

    def send_template(self, to, from_user, template, context):
        '''
        Send a templated/pre-defined message
        '''
        message = Templatizer().render(
            template,
            context,
            base_template=template.email_base_template)

        # this needs to be dynamic and send to best medium
        return self.send(to, message)

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