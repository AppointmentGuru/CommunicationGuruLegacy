from django.db import models
from django.conf import settings

default_delivery = settings.GURU_COMMUNICATIONS.get('DEFAULT_DELIVERY_METHOD', 'EMAIL')
short_message_max_length = settings.GURU_COMMUNICATIONS.get('SHORT_MESSAGE_MAX_LENGTH', 144)

class MessageTemplate(models.Model):
    '''
    A message template defines a basic layout for a communication.

    For example, you might have a MessageTemplate for a Welcome e-mail:

    Hi {{user.first_name}}

    Welcome to our awesome site!
    ---

    In general, every type of transactional email should have a default message template
    defined (by admin typically), then a user can customize the defaul with thier own version
    '''

    def __str__(self):
        return "{}: {}" . format (self.template_id, self.name)

    TYPE_CHOICES = [
        ('EMAIL','Email'),
        ('SMS', 'SMS'),
        ('NOTIFICATION', 'In-app notification')
        ## scope creep. Other backends might be: Twitter, Facebook, Slack, Hipchat ..
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    is_default_template = models.BooleanField(
        default=False,
        help_text='Set to true if this is the base e-mail template you want to use if the user has not specified a custom one'
    )
    template_id = models.SlugField(help_text='This will be used to uniquely identify this type of message')
    email_base_template = models.CharField(max_length=100, blank=True, null=True, default='gurucommunication/base.html')

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    preferred_delivery_method = models.CharField(max_length=10, choices=TYPE_CHOICES, default=default_delivery)

    # only required for email:
    subject = models.CharField(max_length=200, blank=True, null=True)
    long_message = models.TextField(
        help_text="The message to use when space is not limited. e.g.: E-mail"
    )
    short_message = models.TextField(
        help_text="The message to use when space is limited. e.g.: SMS",
        max_length=short_message_max_length
    )

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

class Message(models.Model):
    """
    A log entry for a message send request
    (maybe this should be SendMessageRequest) ?
    """
    template = models.ForeignKey('MessageTemplate')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL)
    backend_used = models.CharField(max_length=100)
    backend_message_id = models.CharField(max_length=100)
    payload_sent = models.TextField()
    payload_received = models.TextField()
    is_successful = models.BooleanField()

    def get_status_from_backend():
        '''
        Call out to the backend service and retrieve the active status
        '''
        pass

