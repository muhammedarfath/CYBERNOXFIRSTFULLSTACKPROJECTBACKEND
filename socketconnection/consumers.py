import json
from socketconnection.serializers import MessageSerializer
from socketconnection.models import Message
from authentication.models import InterestSent, Notification
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from django.db.models import Q
from asgiref.sync import sync_to_async
import logging
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


User = get_user_model()

class NotificationConsumer(WebsocketConsumer):

    def fetch_unread_notification(self, data):
        notifications = Notification.objects.filter(user=self.user, is_read=False)

        content = {
            'option': 'fetch_unread_notification',
            'notifications': [self.message_to_json(notification) for notification in notifications]
        }

        self.send_notification(self.user, content)
        
    def fetch_unread_messages(self, data):
        messages = Message.objects.filter(receiver=self.user, is_read=False)
        
        content = {
            'option': 'fetch_unread_messages',
            'messages': [self.chat_to_json(message) for message in messages]
        }

        self.send_notification(self.user, content)

            

    def interest_sent(self, data):
        user_id = data['userId']
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return

        # Create a notification for the user being liked
        message = f"You have received interest from {self.user.email}!"
        
        
        notification_exists = Notification.objects.filter(
        user=user, sender=self.user, message=message
        ).exists()
        
        
        if not notification_exists:
            notification = Notification.objects.create(user=user, sender=self.user, message=message)

            # Update or create InterestSent object where the logged-in user is the owner
            interest_sent_obj, created = InterestSent.objects.get_or_create(user=self.user)
            interest_sent_obj.interest.add(user)  # Add the other user to the interest field
            interest_sent_obj.save()

            content = {
                'option': 'interest_sent',
                'notification': self.message_to_json(notification),
                'interest_count': interest_sent_obj.like_count()  # Updated interest count
            }

            self.send_notification(user, content)

    def message_to_json(self, notification):
        return {
            'user': notification.user.email,
            'message': notification.message,
            'timestamp': str(notification.timestamp)
        }
        
    def chat_to_json(self, message):
        return {
            'user': message.author.email,
            'message': message.content,
            'timestamp': str(message.timestamp)
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
        'fetch_unread_notification': fetch_unread_notification,
        'fetch_unread_messages':fetch_unread_messages,
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
            
            
            
class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        sender_id, recipient_id = self.room_name.split('_')


        #creating room 
        self.room_group_name = f"chat_{min(sender_id, recipient_id)}_{max(sender_id, recipient_id)}"

        #join the room
        await(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
        
    async def disconnect(self, code):   
        #Leave the room
        await(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        await super().disconnect(code)   
        
        
        
    async def receive(self, text_data):


        # Receive message from WebSocket
        text_data_json = json.loads(text_data)
        print(text_data_json,"new one")
        text = text_data_json['text']
        sender = text_data_json['sender']
        recipient_id = self.room_name.split('_')[1]
        chat_message = await self.save_chat_message(text , sender , recipient_id)

        if chat_message and not chat_message.is_read:
            chat_message.mark_as_read()

        messages = await self.get_messages(sender , recipient_id)
        # Send message to room group
        await(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'messages': messages,
                'sender': sender,
                'message':text
            }
        )         
    
    async def chat_message(self, event):
        # Receive message from room group
        messages = event['messages']
        sender = event['sender']
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'messages': messages,
            'sender': sender,
            'message':message,
        }))




    @database_sync_to_async
    def save_chat_message(self , message , sender_id , recipient_id):
        Message.objects.create(message = message , sender_id = sender_id ,receiver_id = recipient_id)  
        
    @database_sync_to_async
    def get_messages(self,sender ,recipient_id ):

        messages=[]
        for instance in Message.objects.filter(sender__in =[sender , recipient_id] , receiver__in = [sender,recipient_id]):
            messages=MessageSerializer(instance).data
            
        return messages              
    