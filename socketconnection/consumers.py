import json
from socketconnection.models import Message
from authentication.models import Notification
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from django.db.models import Q


User = get_user_model()

class NotificationConsumer(WebsocketConsumer):

    def fetch_unread_notification(self, data):
        notifications = Notification.objects.filter(user=self.user, is_read=False)

        content = {
            'option': 'fetch_unread_notification',
            'notifications': [self.message_to_json(notification) for notification in notifications]
        }

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
        self.send(text_data=json.dumps(event["notification"]))

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
        if data['option'] in self.options:
            self.options[data['option']](self, data)
            
            
            
class ChatConsumer(WebsocketConsumer):
    
    def new_messages(self, data):
        user_id = data['userId']
        message = data['message']
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return

        message = Message.objects.create(author=user, sender=self.user, content=message)

        content = {
            'option': 'new_messages',
            'messages': [self.message_to_json(message)]  
        }

        self.send_notification(user, content)

    
    def message_to_json(self,message):
        return {
            'author':message.author.email,
            'sender':message.sender.email,
            'content':message.content,
            'timestamp':str(message.timestamp)
            
            }  
    
    def send_notification(self, recipient, content):
        recipient_group_name = f"user_{recipient.id}"
        async_to_sync(self.channel_layer.group_send)(
            recipient_group_name, {
                "type": "chat_message",
                "message": content
            }
        )
    
    def chat_message(self, event):
        self.send(text_data=json.dumps(event["message"]))
    
    
    
    def fetch_messages(self, data):
        user_id = data.get('userId')  
        if not user_id:
            return

        messages = Message.objects.filter(
            (Q(author=self.user) & Q(sender_id=user_id)) |  
            (Q(author_id=user_id) & Q(sender=self.user))   
        ).order_by('timestamp')[:100]

        content = {
            'option': 'fetch_messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)
        
        
    def messages_to_json(self,messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result     
    
    def send_message(self,message):
        self.send(text_data=json.dumps( message))    
        
    options = {
        'new_messages': new_messages,
        'fetch_messages': fetch_messages
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
        if data['option'] in self.options:
            self.options[data['option']](self, data)
            
            
