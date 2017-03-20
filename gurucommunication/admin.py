from django.contrib import admin
from .models import MessageTemplate, Message

admin.site.register(MessageTemplate)
admin.site.register(Message)
