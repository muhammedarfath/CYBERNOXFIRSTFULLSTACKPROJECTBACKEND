from authentication.models import Notification
from authentication.serializers import UserSerializer
from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only = True)
    receiver = UserSerializer(read_only = True)
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'message', 'audio', 'is_read', 'timestamp']

class NotificationSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "user", "sender", "message", "is_read", "timestamp","notification_type"]