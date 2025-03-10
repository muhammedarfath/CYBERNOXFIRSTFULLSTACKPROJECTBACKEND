
from django.urls import path
from .views import *

urlpatterns = [
    path('messages/', UserMessagesView.as_view(), name='user-messages'),
    path('unread-notifications/', UnreadNotification.as_view(), name='unread-notifications'),
    path('getmessage/<int:sender_id>/<int:reciever_id>/', GetMessage.as_view(), name='get-message'),
    path('mark-all-as-read/',MarkMessageNotification.as_view(),name='mark-all-as-read'),
    path('message-unread-counts/',UnreadMessageCountView.as_view(),name='message-unread-counts')
]

