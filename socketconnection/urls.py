
from django.urls import path
from .views import *

urlpatterns = [
    path('messages/', UserMessagesView.as_view(), name='user-messages'),
    path('unread-notifications/', UnreadNotification.as_view(), name='unread-notifications'),

]

