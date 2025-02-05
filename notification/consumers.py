import json
from authentication.models import InterestSent, Notification
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync

User = get_user_model()

class NotificationConsumer(WebsocketConsumer):

    def fetch_unread_notification(self, data):
        # Fetch unread notifications for the authenticated user
        notifications = Notification.objects.filter(user=self.user, is_read=False)

        # Prepare the notification data to send back to the client
        content = {
            'option': 'fetch_unread_notification',
            'notifications': [self.message_to_json(notification) for notification in notifications]
        }

        # Send the notifications to the client
        self.send_notification(self.user, content)

    def interest_sent(self, data):
        user_id = data['userId']
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return

        message = f"{self.user.email} has shown interest in you!"

        notification = Notification.objects.create(user=user, sender=self.user, message=message)

        content = {
            'option': 'interest_sent',
            'notification': self.message_to_json(notification)
        }

        # Send the notification to the recipient user
        self.send_notification(user, content)

    def message_to_json(self, notification):
        return {
            'user': notification.user.email,
            'message': notification.message,
            'timestamp': str(notification.timestamp)
        }

    def send_notification(self, recipient, content):
        recipient_group_name = f"user_{recipient.id}"
        async_to_sync(self.channel_layer.group_send)(
            recipient_group_name, {
                "type": "send_notification_event",
                "notification": content
            }
        )

    def send_notification_event(self, event):
        # Send the notification data to the client
        self.send(text_data=json.dumps(event["notification"]))

    # Mapping options to methods
    options = {
        'interest_sent': interest_sent,
        'fetch_unread_notification': fetch_unread_notification
    }

    def connect(self):
        self.user = self.scope["user"]

        if self.user.is_authenticated:
            self.room_group_name = f"user_{self.user.id}"
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )
            self.accept()
        else:
            self.close()

    def disconnect(self, close_code):
        if self.user.is_authenticated:
            self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    def receive(self, text_data):
        data = json.loads(text_data)
        print(data['option'], "check is correct")
        # Dynamically call the appropriate method based on the 'option' field
        if data['option'] in self.options:
            self.options[data['option']](self, data)
