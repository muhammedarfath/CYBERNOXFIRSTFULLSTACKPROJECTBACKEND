from authentication.models import Notification
from authentication.serializers import UserSerializer
from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "author", "sender", "content", "is_read", "timestamp"]

class NotificationSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "user", "sender", "message", "is_read", "timestamp"]