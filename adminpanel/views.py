from django.shortcuts import render
from socketconnection.models import SubscriptionPlan
from authentication.serializers import FetchFamilyInformationSerializer, FetchProfileSerializer, GroomBrideInfoSerializer, PostSerializer
from partnerpreferences.serializers import UserHobbySerializer
from partnerpreferences.models import UserHobby
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from authentication.models import  FamilyInformation, GroomBrideInfo, Post, Profile, User

# Create your views here.



class AdminLogin(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        

        if not email or not password:
            return Response({"detail": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)


        user = authenticate(request, email=email, password=password)
        if user is None:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if the user is a superuser
        if not user.is_superuser:
            return Response({"detail": "Only superusers can log in here."}, status=status.HTTP_403_FORBIDDEN)
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "access": access_token,
            "refresh": str(refresh),
            "email": user.email,
            "userid":user.id,
            "user_type":user.user_type
        }, status=status.HTTP_200_OK)
        
        
        
class FetchAllUsers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Exclude the current user from the list
        users_data = User.objects.exclude(id=user.id)

        serialized_data = []
        for user_obj in users_data:
            # Fetch related data for the user
            user_profile = Profile.objects.filter(user=user_obj).first()
            groom_bride_info = GroomBrideInfo.objects.filter(user=user_obj).first()
            family_info = FamilyInformation.objects.filter(user=user_obj).first()
            user_posts = Post.objects.filter(user=user_obj)
            user_hobbies = UserHobby.objects.filter(user=user_obj).first()

            # Check if the user has an active subscription plan
            subscription_plan = SubscriptionPlan.objects.filter(user=user_obj).first()
            is_subscription_active = (
                subscription_plan.is_subscription_active() if subscription_plan else False
            )

            # Prepare the data
            data = {
                "user_profile": FetchProfileSerializer(user_profile).data if user_profile else None,
                "groom_bride_info": GroomBrideInfoSerializer(groom_bride_info).data if groom_bride_info else None,
                "family_info": FetchFamilyInformationSerializer(family_info).data if family_info else None,
                "posts": PostSerializer(user_posts, many=True).data if user_posts.exists() else None,
                "hobbies": UserHobbySerializer(user_hobbies).data if user_hobbies else None,
                "has_active_subscription": is_subscription_active,
            }

            serialized_data.append(data)

        return Response(serialized_data)
   
   
   
   
def customer_delete(request):
    
    if request.user.user_type !='admin':
        user_id= request.GET.get('user_id')
        user = User.objects.get(id=user_id)
        user.is_deleted = True
        user.save()
        
    else:
        return Response({"detail": "Invalid User."}, status=status.HTTP_401_UNAUTHORIZED)

    