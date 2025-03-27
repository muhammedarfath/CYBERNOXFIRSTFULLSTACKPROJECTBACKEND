from django.shortcuts import render
from adminpanel.serializers import UserVerificationSerializer
from socketconnection.models import SubscriptionPlan
from authentication.serializers import FetchFamilyInformationSerializer, FetchProfileSerializer, GroomBrideInfoSerializer, PostSerializer, UserSerializer
from partnerpreferences.serializers import UserHobbySerializer
from partnerpreferences.models import UserHobby
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from authentication.models import  FamilyInformation, GroomBrideInfo, Post, Profile, User, UserVerification
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password

# Create your views here.


class AdminLogin(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get("email", "").strip()
        password = request.data.get("password", "").strip()
        
        if not email or not password:
            return Response(
                {"detail": "Email and password are required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Debugging output
        print(f"Attempting to authenticate: {email}")
        
        # Try authentication
        user = authenticate(request, username=email, password=password)
        
        # Debugging output
        print(f"Authentication result: {user}")
        if user:
            print(f"User password hash: {user.password}")
            print(f"Password check: {user.check_password(password)}")

        if not user:
            # Additional debugging - check if user exists
            user_exists = User.objects.filter(email=email).exists()
            return Response(
                {
                    "detail": "Invalid credentials",
                    "debug": {
                        "user_exists": user_exists,
                        "email_provided": email,
                        "password_length": len(password)
                    }
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        if user.user_type not in ['superadmin', 'admin']:
            return Response(
                {"detail": "Only administrators can log in here."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "email": user.email,
                "user_type": user.user_type,
                "name": f"{user.first_name} {user.last_name}".strip() or user.username,
                "position": "Super Admin" if user.user_type == "superadmin" else "Admin"
            }
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
    
    
    
class UserVerificationList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.user_type != 'Customer':
            queryset = UserVerification.objects.prefetch_related('identity_proofs').order_by('-created_at')
            serializer = UserVerificationSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response({"detail": "Unauthorized"}, status=403)
    
    
class UserProofVerification(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        if request.user.user_type != 'Customer':
            verification = get_object_or_404(UserVerification, user_id=user_id)
            verification.proof_verified = True
            verification.save()
            return Response({"message": "User proof verified successfully"}, status=status.HTTP_200_OK)


class FetchEmployees(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employees = User.objects.filter(
            user_type__in=['superadmin', 'admin'],
            is_deleted=False
        ).exclude(id=request.user.id)  
        serializer = UserSerializer(employees, many=True)
        return Response(serializer.data)
    
    
class UpdateEmployeeRole(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            employee = User.objects.get(pk=pk, user_type__in=['superadmin', 'admin'])
            new_role = request.data.get('user_type')
            
            
            if new_role not in ['superadmin', 'admin']:
                return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)
                
            employee.user_type = new_role
            employee.save()
            
            return Response({
                'id': employee.id,
                'user_type': employee.user_type,
                'position': 'Super Admin' if employee.user_type == 'superadmin' else 'Admin'
            })
            
        except User.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

class CreateEmployee(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Verify permissions
        if request.data.get('user_type') == 'superadmin' and not request.user.user_type == 'superadmin':
            return Response(
                {"error": "Only superadmins can create other superadmins"},
                status=status.HTTP_403_FORBIDDEN
            )

        password = request.data.get('password')
        
        print(password,"passwordddddddddddddddd")
        if not password:
            return Response(
                {"password": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Prepare data
        employee_data = {
            **request.data,
            'is_staff': True,
            'is_active': True,
            'username': request.data.get('username', request.data.get('email'))  # Fallback to email
        }

        serializer = UserSerializer(data=employee_data)
        
        if serializer.is_valid():
            employee = serializer.save()
            
            # Debugging check
            print(f"Password verification for new user: {employee.check_password(password)}")
            
            return Response({
                'id': employee.id,
                'name': f"{employee.first_name} {employee.last_name}".strip() or employee.username,
                'email': employee.email,
                'position': 'Super Admin' if employee.user_type == 'superadmin' else 'Admin',
                'user_type': employee.user_type
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)