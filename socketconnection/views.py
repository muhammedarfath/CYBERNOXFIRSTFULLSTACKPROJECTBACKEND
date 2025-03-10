from django.shortcuts import render
from partnerpreferences.models import UserHobby
from authentication.models import *
from authentication.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Message, SubscriptionPlan
from .serializers import MessageSerializer, NotificationSerializer
from django.db.models import Q  
import logging
from rest_framework.generics import ListAPIView 
from rest_framework import status


class UserMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Fetch messages where the user is sender or receiver
        messages = Message.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).order_by('-timestamp')

        # Collect other users involved in the conversation
        other_users = set()
        for message in messages:
            if message.sender == user:
                other_users.add(message.receiver)  # ✅ Fixed this line
            else:
                other_users.add(message.sender)

        print(other_users, "check")

        # Fetch latest message for each other user
        latest_messages = []
        for other_user in other_users:
            latest_message = Message.objects.filter(
                (Q(sender=user, receiver=other_user) |
                 Q(sender=other_user, receiver=user))
            ).order_by('-timestamp').first()
            if latest_message:
                latest_messages.append(latest_message)

        print(latest_messages, "doneeee")

        # Fetch profiles for other users
        profiles = Profile.objects.filter(user__in=other_users)

        # Serialize data
        user_serializer = UserSerializer(list(other_users), many=True)
        message_serializer = MessageSerializer(latest_messages, many=True)
        profile_serializer = ProfileSerializer(profiles, many=True)

        return Response({
            "users": user_serializer.data,
            "latest_messages": message_serializer.data,
            "profiles": profile_serializer.data
        })
        
        
logger = logging.getLogger(__name__)

class UnreadNotification(APIView):
    permission_classes = [IsAuthenticated]

    def get_user_full_details(self, user):
        try:
            user_profile = Profile.objects.filter(user=user).first()
            groom_bride_info = GroomBrideInfo.objects.filter(user=user).first()
            family_info = FamilyInformation.objects.filter(user=user).first()
            user_posts = Post.objects.filter(user=user)
            user_hobbies = UserHobby.objects.filter(user=user).first()

            return {
                "user_profile": FetchProfileSerializer(user_profile).data if user_profile else None,
                "groom_bride_info": FetchGroomBrideInfoSerializer(groom_bride_info).data if groom_bride_info else None,
                "family_info": FetchFamilyInformationSerializer(family_info).data if family_info else None,
                "posts": PostSerializer(user_posts, many=True).data if user_posts.exists() else [],
                "hobbies": UserHobbySerializer(user_hobbies).data if user_hobbies else None,
            }
        except Exception as e:
            logger.error(f"Error fetching user details: {e}")
            return {}

    def get(self, request):
        user = request.user

        try:
            # Check if the user has an active subscription
            try:
                subscription = user.subscription
                has_active_subscription = subscription.is_subscription_active()
            except (AttributeError, SubscriptionPlan.DoesNotExist):
                has_active_subscription = False

            # Fetch unread notifications
            received_notifications = Notification.objects.filter(user=user, is_read=False).order_by('-timestamp')
            sent_notifications = Notification.objects.filter(sender=user, is_read=False).order_by('-timestamp')

            # Categorize received notifications
            interest_notifications = received_notifications.filter(notification_type='interest')
            message_notifications = received_notifications.filter(notification_type='message')

            # Prepare response data
            received_data = [
                {
                    "notification": NotificationSerializer(notification).data,
                    "sender_details": self.get_user_full_details(notification.sender)
                }
                for notification in received_notifications
            ]

            sent_data = [
                {
                    "notification": NotificationSerializer(notification).data,
                    "receiver_details": self.get_user_full_details(notification.user)
                }
                for notification in sent_notifications
            ]

            response_data = {
                "has_active_subscription": has_active_subscription,
                "unread_count": received_notifications.count(),
                "interest_unread_count": interest_notifications.count(),  # Count of interest notifications
                "message_unread_count": message_notifications.count(),  # Count of message notifications
                "received_notifications": received_data,
                "sent_notifications": sent_data
            }

            return Response(response_data, status=200)

        except Exception as e:
            logger.error(f"Error in UnreadNotification view: {e}")
            return Response({"error": "Internal Server Error"}, status=500)

        
        
class GetMessage(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    def get_queryset(self):
        sender_id = self.kwargs['sender_id']
        reciever_id = self.kwargs['reciever_id']
        queryset = Message.objects.filter(
            sender__in=[sender_id, reciever_id],
            receiver__in=[sender_id, reciever_id]
        ).order_by('timestamp')
        for message in queryset:
            print(message.is_read)
            if message.receiver.id == self.request.user.id:
                message.is_read = True
                message.save()

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)        
        
class MarkMessageNotification(APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request, *args, **kwargs):
        user = request.user  
        Notification.objects.filter(
            user=user, 
            notification_type='message', 
            is_read=False
        ).update(is_read=True)
        
        return Response({"status": "success"}, status=status.HTTP_200_OK)     
    
class UnreadMessageCountView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request, *args, **kwargs):
        receiver_id = request.user.id  # ID of the authenticated user (receiver)

        # Get unread message counts for each sender
        unread_counts = (
            Message.objects
            .filter(receiver_id=receiver_id, is_read=False)
            .values('sender_id')
            .annotate(unread_count=models.Count('id'))
        )
        
        # Convert to a dictionary for easy lookup
        unread_counts_dict = {
            item['sender_id']: item['unread_count'] for item in unread_counts
        }

        return Response(unread_counts_dict, status=status.HTTP_200_OK)       
