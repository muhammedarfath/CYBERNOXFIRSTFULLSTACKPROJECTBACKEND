from django.contrib import admin
from .models import Message

from authentication.models import InterestSent, Notification

# Register your models here.


admin.site.register(Notification)
admin.site.register(InterestSent)
admin.site.register(Message)
