from authentication.serializers import UserSerializer
from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "author", "sender", "content", "is_read", "timestamp"]

