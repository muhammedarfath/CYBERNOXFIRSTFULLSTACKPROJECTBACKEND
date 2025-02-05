from django.contrib import admin

from authentication.models import InterestSent, Notification

# Register your models here.


admin.site.register(Notification)
admin.site.register(InterestSent)
