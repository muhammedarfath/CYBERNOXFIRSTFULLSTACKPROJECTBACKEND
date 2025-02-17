from django.shortcuts import render
from authentication.models import Notification
from authentication.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Message, SubscriptionPlan
from .serializers import MessageSerializer, NotificationSerializer
from django.db.models import Q  

class UserMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        print(f"Current User: {user}")

        messages = Message.objects.filter(
            Q(author=user) | Q(sender=user)
        ).order_by('-timestamp')

        other_users = set()
        for message in messages:
            if message.author == user:
                other_users.add(message.sender) 
            else:
                other_users.add(message.author)  


        latest_messages = []
        for other_user in other_users:
            latest_message = Message.objects.filter(
                Q(author=user, sender=other_user) | Q(author=other_user, sender=user)
            ).order_by('-timestamp').first()  
            if latest_message:
                latest_messages.append(latest_message)

        user_serializer = UserSerializer(list(other_users), many=True)
        message_serializer = MessageSerializer(latest_messages, many=True)

        return Response({
            "users": user_serializer.data,
            "latest_messages": message_serializer.data
        })
        
        
class UnreadNotification(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            subscription = user.subscription
            has_active_subscription = subscription.is_subscription_active()
        except SubscriptionPlan.DoesNotExist:
            has_active_subscription = False
            
        received_notifications = Notification.objects.filter(user=user, is_read=False).order_by('-timestamp')
        sent_notifications = Notification.objects.filter(sender=user, is_read=False).order_by('-timestamp')

        response_data = {
            "has_active_subscription": has_active_subscription,
            "unread_count": received_notifications.count(),
            "received_notifications": NotificationSerializer(received_notifications, many=True).data,
            "sent_notifications": NotificationSerializer(sent_notifications, many=True).data
        }
        
        return Response(response_data, status=200)