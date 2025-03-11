import base64
import json
from socketconnection.utils import send_interest_email, send_message_email
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
from django.core.files.base import ContentFile


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

        # Create a notification for the user being liked
        message = f"You have received interest from {self.user.email}!"
        
        
        notification_exists = Notification.objects.filter(
        user=user, sender=self.user, message=message,notification_type='interest'
        ).exists()
        
        
        if not notification_exists:
            notification = Notification.objects.create(user=user, sender=self.user, message=message,notification_type='interest')

            interest_sent_obj, created = InterestSent.objects.get_or_create(user=self.user)
            interest_sent_obj.interest.add(user)  
            interest_sent_obj.save()
            send_interest_email(user.email, user)

            content = {
                'option': 'interest_sent',
                'notification': self.message_to_json(notification),
                'interest_count': interest_sent_obj.like_count() ,
                'notification_type': 'interest' 
            }

            self.send_notification(user, content)

    def message_to_json(self, notification):
        return {
            'user': notification.user.email,
            'message': notification.message,
            'timestamp': str(notification.timestamp),
            'notification_type':notification.notification_type,
            
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
        print(f"Received notification event: {event}")
        self.send(text_data=json.dumps(event["notification"]))
        
        

    options = {
        'interest_sent': interest_sent,
        'fetch_unread_notification': fetch_unread_notification,
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
            
class MessageNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.notification_group_name = f'notifications_{self.user_id}'

        # Join notification group
        await self.channel_layer.group_add(
            self.notification_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave notification group
        await self.channel_layer.group_discard(
            self.notification_group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        # Send notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': event['message'],
            'sender': event['sender'],
        }))            
             
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.sender_id, self.recipient_id = self.room_name.split('_')

        # Create room name
        self.room_group_name = f"chat_{min(self.sender_id, self.recipient_id)}_{max(self.sender_id, self.recipient_id)}"

        # Join the room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Notify that the user is online
        await self.update_user_status(self.sender_id, "online")
        await self.broadcast_user_status(self.sender_id, "online")

    async def disconnect(self, close_code):
        # Leave the room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Notify that the user is offline
        await self.update_user_status(self.sender_id, "offline")
        await self.broadcast_user_status(self.sender_id, "offline")

        await super().disconnect(close_code)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text = text_data_json.get('text')
        sender = text_data_json.get('sender')
        is_audio = text_data_json.get('isAudio')
        recipient_id = self.room_name.split('_')[1]

        # Check if the recipient has blocked the sender
        is_blocked = await self.is_user_blocked(sender, recipient_id)
        if is_blocked:
            # Notify the sender that they are blocked
            await self.send(text_data=json.dumps({
                'type': 'blocked',
                'message': 'You are blocked by the recipient. Message not sent.',
            }))
            return  # Exit the function without sending the message

        if is_audio:
            audio_data = is_audio
            chat_message = await self.save_audio_message(audio_data, sender, recipient_id)
        else:
            chat_message = await self.save_chat_message(text, sender, recipient_id)

        if chat_message and not chat_message.is_read:
            await database_sync_to_async(chat_message.mark_as_read)()

        messages = await self.get_messages(sender, recipient_id)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'messages': messages,
                'sender': sender,
                'message': text if not is_audio else None,
                'isAudio': is_audio,
            }
        )

        await self.send_notification_to_recipient(sender, recipient_id, is_audio, text if not is_audio else "Audio message")

    @database_sync_to_async
    def is_user_blocked(self, sender_id, recipient_id):
        """
        Check if the recipient has blocked the sender.
        """
        recipient = User.objects.get(id=recipient_id)
        return recipient.blocked_users.filter(id=sender_id).exists()

    async def send_notification_to_recipient(self, sender_id, recipient_id, is_audio, message_text):
        print(f"Sending notification to recipient {recipient_id} from sender {sender_id}")
        # Fetch sender and recipient details
        sender = await self.get_user(sender_id)
        recipient = await self.get_user(recipient_id)

        # Create notification message
        notification_message = f"New message from {sender.email}: {message_text}"

        # Send notification to the recipient's notification group
        await self.channel_layer.group_send(
            f'notifications_{recipient_id}',
            {
                'type': 'send_notification',
                'message': notification_message,
                'sender': sender.email,
            }
        )
        await self.create_notification(recipient, sender, notification_message)

    async def chat_message(self, event):
        # Receive message from room group
        messages = event['messages']
        sender = event['sender']
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'messages': messages,
            'sender': sender,
            'message': message,
        }))

    async def user_status(self, event):
        # Handle user status updates
        user_id = event['user_id']
        status = event['status']

        # Send status update to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'status_update',
            'user_id': user_id,
            'status': status
        }))

    @database_sync_to_async
    def save_audio_message(self, audio_data, sender_id, recipient_id):
        format, audio_str = audio_data.split(';base64,')
        ext = format.split('/')[-1]
        audio_file = ContentFile(base64.b64decode(audio_str), name=f'audio_{sender_id}_{recipient_id}.{ext}')

        message = Message.objects.create(
            sender_id=sender_id,
            receiver_id=recipient_id,
            audio=audio_file,
            is_read=False
        )
        return message

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def create_notification(self, recipient, sender, message):
        notification = Notification.objects.create(
            user=recipient,
            sender=sender,
            message=message,
            notification_type='message'
        )
        return notification

    @database_sync_to_async
    def save_chat_message(self, message, sender_id, recipient_id):
        Message.objects.create(message=message, sender_id=sender_id, receiver_id=recipient_id)

    @database_sync_to_async
    def get_messages(self, sender, recipient_id):
        messages = []
        for instance in Message.objects.filter(sender__in=[sender, recipient_id], receiver__in=[sender, recipient_id]):
            messages = MessageSerializer(instance).data
        return messages

    @database_sync_to_async
    def update_user_status(self, user_id, status):
        # Update the user's status in the database
        user = User.objects.get(id=user_id)
        user.is_online = (status == "online")
        user.save()

    async def broadcast_user_status(self, user_id, status):
        # Broadcast the user's status to the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_status',
                'user_id': user_id,
                'status': status
            }
        )