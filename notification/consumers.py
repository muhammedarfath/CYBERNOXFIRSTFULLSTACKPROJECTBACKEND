import json
from authentication.models import InterestSent, Notification
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync

User = get_user_model()

class NotificationConsumer(WebsocketConsumer):
    
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
        
        self.send_notificaton(user, content)

    
    
    def message_to_json(self,notification):
        return {
            'user':notification.user.email,
            'message':notification.message,
            'timestamp':str(notification.timestamp)
            }   

    def send_notificaton(self, recipient, content):    
        recipient_group_name = f"user_{recipient.id}" 
        async_to_sync(self.channel_layer.group_send)(
            recipient_group_name, {
                "type": "send_notification_event", 
                "notification": content
            }
        )
        
    def send_notification_event(self, event):
        print(event,"call")
        self.send(text_data=json.dumps(event["notification"]))
          
            
    options ={
        'interest_sent':interest_sent,
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
           self.channel_layer.group_discard(self.group_name, self.channel_name)

    def receive(self, text_data):
        data = json.loads(text_data)
        print(data['option'],"check is correct")
        self.options[data['option']](self, data)
                

                    
