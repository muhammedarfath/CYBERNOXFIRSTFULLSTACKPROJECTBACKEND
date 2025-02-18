from partnerpreferences.models import PartnerExpectation, UserHobby
from rest_framework import generics, status
from rest_framework.response import Response
from .models import AnnualIncome, Blood, BodyType, CurrentLiving, Education, Employment, FamilyStatus, FamilyType, Hair, HairType, HomeType, MaritalStatus, Occupation, Political, Polygamy, Post, ReligiousServices, Religiousness, Skin, User
from .serializers import BloodGroupSerializer, BodySerializer, CreateForSerializer, EducationSerializer, EmployementSerializer, FamilyStatusSerializer, FamilyTypeSerializer, FetchFamilyInformationSerializer, FetchGroomBrideInfoSerializer, FetchProfileSerializer, FullProfileSerializer, GenderSerializer, HairColorSerializer, HairTypeSerializer, HomeTypeSerializer, LivingSituationSerializer, MaritalSerializer, OccupationSerializer, PoliticalViewSerializer, PolygamySerializer, PostSerializer, ReligiousnesServicesSerializer, ReligiousnessSerializer, SkinColorSerializer, UserProfileUpdateSerializer, UserSerializer
from .models import Profile,GroomBrideInfo
from .serializers import ProfileSerializer,GroomBrideInfoSerializer
from .models import FamilyInformation,Gender,CreateFor
from .serializers import FamilyInformationSerializer,ReligionSerializer, CasteSerializer,AnnualIncomeSerializer
from rest_framework.views import APIView
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import Profile, GroomBrideInfo, FamilyInformation,Religion, Caste
from datetime import datetime
from rest_framework.generics import UpdateAPIView
from django.shortcuts import get_object_or_404

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        mobile = request.data.get("mobileno")
        email = request.data.get("email")
        password = request.data.get("password")
        if not mobile and not email:
            return Response({"detail": "Mobile number or email is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user by either mobile or email
        user = None
        if mobile:
            user = authenticate(request, mobileno=mobile, password=password)
        elif email:
            user = authenticate(request, email=email, password=password)
        if user is None:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "access": access_token,
            "refresh": str(refresh),
            "email": user.email,
            "userid":user.id,
        }, status=status.HTTP_200_OK)
        
        
        
class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        user = get_object_or_404(User, email=email)
        
        # Generate reset token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

        # Send email
        send_mail(
            subject="Password Reset Request",
            message = f"""
            Hello {user.email},

            We received a request to reset your password. If you didn't request this, you can ignore this email.

            Click the link below to reset your password:
            {reset_link}

            If you have any issues, contact our support team.

            Best Regards,  
            The YourWebsite Team  
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        return Response({"message": "Password reset link sent to email."}, status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({"error": "Invalid link."}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get("password")
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK) 


class GenderView(APIView):
    def get(self, request):
        try:
            genders = Gender.objects.all()
            gender_serializer = GenderSerializer(genders, many=True)
            return Response(gender_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateForView(APIView):
    def get(self, request):
        try:
            create_for = CreateFor.objects.all()
            create_for_serializer = CreateForSerializer(create_for, many=True)
            return Response(create_for_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def create(self, request, *args, **kwargs):
        # Simple validation: Check if email already exists
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return Response(
                {'detail': 'Email is already taken.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Simple validation: Check if mobile number already exists
        mobileno = request.data.get('mobileno')
        if User.objects.filter(mobileno=mobileno).exists():
            return Response(
                {'detail': 'Mobile number is already registered.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # If email and mobile number are unique, proceed with creating the user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({
            'user': serializer.data,
            'access': access_token,
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
   
    
class CheckBasicDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"profile_complete": False, "error": "User not authenticated"}, status=401)

        profile_exists = Profile.objects.filter(user=request.user).exists()
        groom_bride_info_exists = GroomBrideInfo.objects.filter(user=request.user).exists()
        family_info_exists = FamilyInformation.objects.filter(user=request.user).exists()

        profile_complete = profile_exists and groom_bride_info_exists and family_info_exists
        return Response({"profile_complete": profile_complete})

   
class ProfileGroomBrideFamilyCreateView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        if Profile.objects.filter(user=user_id).exists():
            return Response(
                {'detail': 'User already has a profile.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if GroomBrideInfo.objects.filter(user=user_id).exists():
            return Response(
                {'detail': 'User already has a GroomBrideInfo profile.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if FamilyInformation.objects.filter(user=user_id).exists():
            return Response(
                {'detail': 'User already has a FamilyInformation profile.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        flattened_data = {
            'user': request.data.get('user'),
            'name': request.data.get('basicdetails', {}).get('groomName'),
            'date_of_birth': self.parse_date_of_birth(request.data.get('basicdetails', {}).get('dateOfBirth')),
            'marital_status': request.data.get('basicdetails', {}).get('selectedMarital'),
            'religion': request.data.get('basicdetails', {}).get('selectedReligion'),
            'mother_tongue': request.data.get('basicdetails', {}).get('selectedTongue'),
            'caste': request.data.get('basicdetails', {}).get('selectedCaste'),
            'height': request.data.get('basicdetails', {}).get('height'),
            'weight': request.data.get('basicdetails', {}).get('weight'),
            'body_type': request.data.get('basicdetails', {}).get('selectBodyType'),
            'physical_challenges': request.data.get('basicdetails', {}).get('physicalStatus'),
            'physical_status': request.data.get('basicdetails', {}).get('typeofphysicalStatus'),
            
            # GroomBrideInfo fields
            'user': request.data.get('user'),
            'country': request.data.get('groomBrideDetails', {}).get('country'),
            'state': request.data.get('groomBrideDetails', {}).get('state'),
            'city': request.data.get('groomBrideDetails', {}).get('city'),
            'family_live': request.data.get('groomBrideDetails', {}).get('familyLive'),
            'occupation': request.data.get('groomBrideDetails', {}).get('occupation'),
            'other_occupation': request.data.get('groomBrideDetails', {}).get('otherOccupation'),
            'education': request.data.get('groomBrideDetails', {}).get('highestEducation'),
            'employment': request.data.get('groomBrideDetails', {}).get('employedIn'),
            'income': request.data.get('groomBrideDetails', {}).get('annualIncome'),
            'college_name': request.data.get('groomBrideDetails', {}).get('collegeName'),
            
            # FamilyInformation fields
            'user': request.data.get('user'),
            'family_type': request.data.get('formData', {}).get('familyType'),
            'family_status': request.data.get('formData', {}).get('familyStatus'),
            'father_name': request.data.get('formData', {}).get('fatherName'),
            'father_occupation': request.data.get('formData', {}).get('fatherOccupation'),
            'mother_occupation': request.data.get('formData', {}).get('motherOccupation'),
            'number_of_brothers': request.data.get('formData', {}).get('brothers'),
            'number_of_sisters': request.data.get('formData', {}).get('sisters'),
            'married_brothers': request.data.get('formData', {}).get('marriedBrothers'),
            'married_sisters': request.data.get('formData', {}).get('marriedSisters'),
            'family_description': request.data.get('formData', {}).get('familyDescription'),
        }

        # Create Profile
        profile_serializer = ProfileSerializer(data=flattened_data)
        profile_serializer.is_valid(raise_exception=True)
        profile = profile_serializer.save()

        # Create GroomBrideInfo
        groom_bride_info_serializer = GroomBrideInfoSerializer(data=flattened_data)
        groom_bride_info_serializer.is_valid(raise_exception=True)
        groom_bride_info = groom_bride_info_serializer.save(user=profile.user)

        # Create FamilyInformation
        family_info_serializer = FamilyInformationSerializer(data=flattened_data)
        family_info_serializer.is_valid(raise_exception=True)
        family_info = family_info_serializer.save(user=profile.user)

        # Combine all data into one response
        response_data = {
            'profile': profile_serializer.data,
            'groom_bride_info': groom_bride_info_serializer.data,
            'family_information': family_info_serializer.data
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    def parse_date_of_birth(self, date_str):
        try:
            return datetime.strptime(date_str, "%Y-%B-%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Please use 'YYYY-Month-DD'.")

class ReligionListView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self, request):
        religions = Religion.objects.all()
        serializer = ReligionSerializer(religions, many=True)
        return Response(serializer.data)

class CasteListView(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request, religion_id):
        castes = Caste.objects.filter(religion_id=religion_id)
        serializer = CasteSerializer(castes, many=True)
        return Response(serializer.data) 
    
class MaritalListView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self, request):
        maritals = MaritalStatus.objects.all()
        serializer = MaritalSerializer(maritals, many=True)
        return Response(serializer.data)  
    
    
class BodyListView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self, request):
        type = BodyType.objects.all()
        serializer = BodySerializer(type, many=True)
        return Response(serializer.data)               
    
    
class EmployementsListView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self, request):
        type = Employment.objects.all()
        serializer = EmployementSerializer(type, many=True)
        return Response(serializer.data)       
    
class EducationListView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self, request):
        type = Education.objects.all()
        serializer = EducationSerializer(type, many=True)
        return Response(serializer.data) 
    
    
class OccupationListView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self, request):
        type = Occupation.objects.all()
        serializer = OccupationSerializer(type, many=True)
        return Response(serializer.data)   
    
    
    
class FamilyTypeListView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self, request):
        type = FamilyType.objects.all()
        serializer = FamilyTypeSerializer(type, many=True)
        return Response(serializer.data)                                                 


    
class FamilyStatusListView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self, request):
        type = FamilyStatus.objects.all()
        serializer = FamilyStatusSerializer(type, many=True)
        return Response(serializer.data)    
    
    
class AnnualIncomeListView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self, request):
        type = AnnualIncome.objects.all()
        serializer = AnnualIncomeSerializer(type, many=True)
        return Response(serializer.data)
    
    
    
    
class FetchProfileDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_profile = Profile.objects.get(user=request.user)
            groom_bride_info = GroomBrideInfo.objects.get(user=request.user)
            family_info = FamilyInformation.objects.get(user=request.user)
            
            try:
                user_hobby = UserHobby.objects.get(user=request.user)
                partner_preferences = PartnerExpectation.objects.get(user=request.user)
            except UserHobby.DoesNotExist:
                user_hobby = None  
                partner_preferences = None
            
            full_profile_data = {
                'user_profile': user_profile,
                'groom_bride_info': groom_bride_info,
                'family_info': family_info,
                'user_hobby': user_hobby,
                'partner_preferences' :partner_preferences,
            }

            serializer = FullProfileSerializer(full_profile_data)
            return Response(serializer.data, status=200)
        
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=404)
        except GroomBrideInfo.DoesNotExist:
            return Response({"error": "GroomBrideInfo not found"}, status=404)
        except FamilyInformation.DoesNotExist:
            return Response({"error": "FamilyInformation not found"}, status=404)
        
class PostCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(user=request.user).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class PostDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id, *args, **kwargs):
        try:
            post = Post.objects.get(id=post_id)
            if post.user != request.user:
                return Response({"detail": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)
            post.delete()
            return Response({"detail": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)    
        
        
class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile picture updated successfully!"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    

class FetchUsers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        gender = user.gender

        if gender and gender.name == 'Male': 
            users_data = User.objects.filter(gender__name='Female').order_by('-date_joined')
        elif gender and gender.name == 'Female':  
            users_data = User.objects.filter(gender__name='Male').order_by('-date_joined')
        else:
            users_data = User.objects.none()

        serialized_data = []
        for user_obj in users_data:
            user_profile = Profile.objects.filter(user=user_obj).first()
            groom_bride_info = GroomBrideInfo.objects.filter(user=user_obj).first()
            family_info = FamilyInformation.objects.filter(user=user_obj).first()
            user_posts = Post.objects.filter(user=user_obj)


            data = {
                "user_profile": FetchProfileSerializer(user_profile).data if user_profile else None,
                "groom_bride_info": FetchGroomBrideInfoSerializer(groom_bride_info).data if groom_bride_info else None,
                "family_info": FetchFamilyInformationSerializer(family_info).data if family_info else None,
                "posts": PostSerializer(user_posts, many=True).data if user_posts.exists() else None,  # Serialize posts

            }

            serialized_data.append(data)

        return Response(serialized_data)
    



class UpdateLanguagesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        action = request.data.get("action") 
        languages_spoken = request.data.get("languages_spoken")

        if not languages_spoken:
            return Response({"error": "No languages provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            profile = Profile.objects.get(user=request.user)

            existing_languages = set(profile.languages_spoken.split(",") if profile.languages_spoken else [])

            if isinstance(languages_spoken, str):
                new_languages = {lang.strip() for lang in languages_spoken.split(",")}
            elif isinstance(languages_spoken, list):
                new_languages = {lang.strip() for lang in languages_spoken}
            else:
                return Response({"error": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST)

            if action == "add":
                updated_languages = existing_languages.union(new_languages)
            elif action == "remove":
                updated_languages = existing_languages - new_languages
            else:
                return Response({"error": "Invalid action specified"}, status=status.HTTP_400_BAD_REQUEST)

            profile.languages_spoken = ",".join(updated_languages)
            profile.save()

            return Response({"message": "Languages updated successfully!"}, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response({"error": "Profile not found!"}, status=status.HTTP_404_NOT_FOUND)

    permission_classes = [IsAuthenticated]

    def post(self, request):
        action = request.data.get("action")  
        languages_spoken = request.data.get("languages_spoken")

        if not languages_spoken:
            return Response({"error": "No languages provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            profile = Profile.objects.get(user=request.user)

            existing_languages = set(profile.languages_spoken.split(",") if profile.languages_spoken else [])

            if isinstance(languages_spoken, str):
                new_languages = {lang.strip() for lang in languages_spoken.split(",")}
            elif isinstance(languages_spoken, list):
                new_languages = {lang.strip() for lang in languages_spoken}
            else:
                return Response({"error": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST)

            if action == "add":
                updated_languages = existing_languages.union(new_languages)
            elif action == "remove":
                updated_languages = existing_languages - new_languages
            else:
                return Response({"error": "Invalid action specified"}, status=status.HTTP_400_BAD_REQUEST)

            profile.languages_spoken = ",".join(updated_languages)
            profile.save()

            return Response({"message": "Languages updated successfully!"}, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response({"error": "Profile not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        
        
class UpdateLocationView(UpdateAPIView):
    queryset = GroomBrideInfo.objects.all()
    serializer_class = GroomBrideInfoSerializer
    permission_classes = [IsAuthenticated]  

    def get_object(self):
        user = self.request.user
        return GroomBrideInfo.objects.get(user=user)

    def update(self, request, *args, **kwargs):

        instance = self.get_object()

        instance.present_country = request.data.get("country", instance.present_country)
        instance.present_state = request.data.get("state", instance.present_state)
        instance.present_city = request.data.get("city", instance.present_city)

        instance.save()

        response_data = {
            "message": "Location updated successfully.",
            "updated_location": {
                "country": instance.present_country,
                "state": instance.present_state,
                "city": instance.present_city
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
    
class UpdateSecondaryView(UpdateAPIView):    
    queryset = GroomBrideInfo.objects.all()
    serializer_class = GroomBrideInfoSerializer
    permission_classes = [IsAuthenticated]  

    def get_object(self):
        user = self.request.user
        return GroomBrideInfo.objects.get(user=user)

    def update(self, request, *args, **kwargs):

        instance = self.get_object()

        instance.secondary_mobileno = request.data.get("secondary_mobileno")

        instance.save()

        return Response({"message": "Location updated successfully."}, status=status.HTTP_200_OK)
    
    


class UpdateTimeToCallView(UpdateAPIView):    
    queryset = GroomBrideInfo.objects.all()
    serializer_class = GroomBrideInfoSerializer
    permission_classes = [IsAuthenticated]  

    def get_object(self):
        return GroomBrideInfo.objects.get(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        time_to_call = request.data.get("time_to_call")
        if not time_to_call:
            return Response({"error": "Time to call is required"}, status=status.HTTP_400_BAD_REQUEST)

        instance.time_to_call = time_to_call
        instance.save()

        return Response({"message": "Time to call updated successfully."}, status=status.HTTP_200_OK)
    
class UpdateFullAddressView(UpdateAPIView):    
    queryset = GroomBrideInfo.objects.all()
    serializer_class = GroomBrideInfoSerializer
    permission_classes = [IsAuthenticated]  

    def get_object(self):
        return GroomBrideInfo.objects.get(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        full_address = request.data.get("full_address")
        
        if not full_address:
            return Response({"error": "Full address is required"}, status=status.HTTP_400_BAD_REQUEST)

        instance.addres = full_address
        instance.save()

        return Response({"message": "Full address updated successfully."}, status=status.HTTP_200_OK)            
    
      
        
class UpdateCompany(UpdateAPIView):    
    queryset = GroomBrideInfo.objects.all()
    serializer_class = GroomBrideInfoSerializer
    permission_classes = [IsAuthenticated]  

    def get_object(self):
        return GroomBrideInfo.objects.get(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        company_name = request.data.get("company_name")
        
        if not company_name:
            return Response({"error": "Full company is required"}, status=status.HTTP_400_BAD_REQUEST)

        instance.company_name = company_name
        instance.save()

        return Response({"message": "Full company updated successfully."}, status=status.HTTP_200_OK)        
    
    
    
class UpdateExperience(UpdateAPIView):    
    queryset = GroomBrideInfo.objects.all()
    serializer_class = GroomBrideInfoSerializer
    permission_classes = [IsAuthenticated]  

    def get_object(self):
        return GroomBrideInfo.objects.get(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        experience = request.data.get("experience")
        
        if not experience:
            return Response({"error": "Full company is required"}, status=status.HTTP_400_BAD_REQUEST)

        instance.experience = experience
        instance.save()

        return Response({"message": "Full company updated successfully."}, status=status.HTTP_200_OK)   
    
    
    
class FetchReligiousness(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        religiousness_options = Religiousness.objects.all()
        serialized_data = ReligiousnessSerializer(religiousness_options, many=True)
        return Response({"options": serialized_data.data}, status=status.HTTP_200_OK)



class UpdateReligiousness(UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        religiousness_name = request.data.get("religiousness")

        if not religiousness_name:
            return Response({"error": "Religiousness is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            religiousness = Religiousness.objects.get(name=religiousness_name)
        except Religiousness.DoesNotExist:
            return Response({"error": "Invalid religiousness value"}, status=status.HTTP_400_BAD_REQUEST)

        instance.religiousness = religiousness
        instance.save()

        return Response({"message": "Religiousness updated successfully."}, status=status.HTTP_200_OK)
    
    
class FetchReligiousnesServices(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        religiousness_options = ReligiousServices.objects.all()
        serialized_data = ReligiousnesServicesSerializer(religiousness_options, many=True)
        return Response({"options": serialized_data.data}, status=status.HTTP_200_OK)



class UpdateReligiousnesServices(UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        religiousnes_services = request.data.get("religiousnes_services")

        if not religiousnes_services:
            return Response({"error": "Religiousness is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            religiousnes_services = ReligiousServices.objects.get(name=religiousnes_services)
        except Religiousness.DoesNotExist:
            return Response({"error": "Invalid religiousness value"}, status=status.HTTP_400_BAD_REQUEST)

        instance.religious_services = religiousnes_services
        instance.save()

        return Response({"message": "Religiousness updated successfully."}, status=status.HTTP_200_OK)    
    


class FetchPolygamyOptions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        polygamy_options = Polygamy.objects.all()  
        serialized_data = PolygamySerializer(polygamy_options, many=True) 
        return Response({"options": serialized_data.data}, status=status.HTTP_200_OK)


class UpdatePolygamyPreference(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        polygamy_preference = request.data.get("polygamy")

        if not polygamy_preference:
            return Response({"error": "Polygamy preference is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            polygamy_option = Polygamy.objects.get(name=polygamy_preference)
        except Polygamy.DoesNotExist:
            return Response({"error": "Invalid polygamy preference value"}, status=status.HTTP_400_BAD_REQUEST)

        instance.polygamy = polygamy_option
        instance.save()

        return Response({"message": "Polygamy preference updated successfully."}, status=status.HTTP_200_OK)
    
    
class FetchPoliticalViewOptions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        political_view_options = Political.objects.all() 
        serialized_data = PoliticalViewSerializer(political_view_options, many=True)
        return Response({"options": serialized_data.data}, status=status.HTTP_200_OK)


class UpdatePoliticalViewPreference(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        political_view_preference = request.data.get("political_view")

        if not political_view_preference:
            return Response({"error": "Political view preference is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            political_view_option = Political.objects.get(name=political_view_preference)
        except Political.DoesNotExist:
            return Response({"error": "Invalid political view preference value"}, status=status.HTTP_400_BAD_REQUEST)

        instance.political_View = political_view_option
        instance.save()

        return Response({"message": "Political view preference updated successfully."}, status=status.HTTP_200_OK)   
    


class FetchSkinColorOptions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        skin_color_options = Skin.objects.all()  
        serialized_data = SkinColorSerializer(skin_color_options, many=True)
        return Response({"options": serialized_data.data}, status=status.HTTP_200_OK)


class UpdateSkinColorPreference(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)  

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        skin_color_preference = request.data.get("skin_color")

        if not skin_color_preference:
            return Response({"error": "Skin color preference is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            skin_color_option = Skin.objects.get(name=skin_color_preference)
        except Skin.DoesNotExist:
            return Response({"error": "Invalid skin color preference value"}, status=status.HTTP_400_BAD_REQUEST)

        instance.skin_color = skin_color_option  
        instance.save()

        return Response({"message": "Skin color preference updated successfully."}, status=status.HTTP_200_OK)
     
     
class FetchBloodGroupOptions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        blood_group_options = Blood.objects.all()  
        serialized_data = BloodGroupSerializer(blood_group_options, many=True)
        return Response({"options": serialized_data.data}, status=status.HTTP_200_OK)
    
    
class UpdateBloodGroupPreference(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user) 

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        blood_group_preference = request.data.get("blood_group")

        if not blood_group_preference:
            return Response({"error": "Blood group preference is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            blood_group_option = Blood.objects.get(name=blood_group_preference)  
        except Blood.DoesNotExist:
            return Response({"error": "Invalid blood group preference value"}, status=status.HTTP_400_BAD_REQUEST)

        instance.blood_group = blood_group_option  
        instance.save()

        return Response({"message": "Blood group preference updated successfully."}, status=status.HTTP_200_OK)
    
    
class FetchHairColorOptions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        hair_color_options = Hair.objects.all()  
        serialized_data = HairColorSerializer(hair_color_options, many=True)
        return Response({"options": serialized_data.data}, status=status.HTTP_200_OK)


class UpdateHairColorPreference(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)  

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        hair_color_preference = request.data.get("hair_color")

        if not hair_color_preference:
            return Response({"error": "Hair color preference is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            hair_color_option = Hair.objects.get(name=hair_color_preference)  
        except Hair.DoesNotExist:
            return Response({"error": "Invalid hair color preference value"}, status=status.HTTP_400_BAD_REQUEST)

        instance.hair_color = hair_color_option  
        instance.save()

        return Response({"message": "Hair color preference updated successfully."}, status=status.HTTP_200_OK)
    
    
class FetchHairTypeOptions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        hair_type_options = HairType.objects.all()
        serialized_data = HairTypeSerializer(hair_type_options, many=True)
        return Response({"options": serialized_data.data}, status=status.HTTP_200_OK)


class UpdateHairTypePreference(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)  

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        hair_type_preference = request.data.get("hair_type")

        if not hair_type_preference:
            return Response({"error": "Hair type preference is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            hair_type_option = HairType.objects.get(name=hair_type_preference)
        except HairType.DoesNotExist:
            return Response({"error": "Invalid hair type preference value"}, status=status.HTTP_400_BAD_REQUEST)

        instance.hair_type = hair_type_option  
        instance.save()

        return Response({"message": "Hair type preference updated successfully."}, status=status.HTTP_200_OK)         
    
    
class UpdateAppearance(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)  

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        appearance = request.data.get("appearance")

        if not appearance:
            return Response({"error": "appearance is required"}, status=status.HTTP_400_BAD_REQUEST)

        instance.appearance = appearance  
        instance.save()

        return Response({"message": "Hair type preference updated successfully."}, status=status.HTTP_200_OK)   
    
    
    
class FetchHomeTypeOptions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        home_type_options = HomeType.objects.all()
        serialized_data = HomeTypeSerializer(home_type_options, many=True)
        return Response({"options": serialized_data.data}, status=status.HTTP_200_OK)


class UpdateHomeTypePreference(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return FamilyInformation.objects.get(user=self.request.user)  
    

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        home_type_preference = request.data.get("home_type")
        
        print(home_type_preference)

        if not home_type_preference:
            return Response({"error": "Home type preference is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            home_type_option = HomeType.objects.get(name=home_type_preference)
        except HomeType.DoesNotExist:
            return Response({"error": "Invalid home type preference value"}, status=status.HTTP_400_BAD_REQUEST)

        instance.home_type = home_type_option  
        instance.save()

        return Response({"message": "Home type preference updated successfully."}, status=status.HTTP_200_OK)         
    
    
    
    
              
class FetchLivingSituationOptions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        living_situations = CurrentLiving.objects.all()
        serialized_data = LivingSituationSerializer(living_situations, many=True)
        return Response({"options": serialized_data.data}, status=status.HTTP_200_OK)


class UpdateLivingSituationPreference(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return FamilyInformation.objects.get(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        living_situation= request.data.get("living_situation")

        if not living_situation:
            return Response({"error": "Living situation preference is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            living_situation = CurrentLiving.objects.get(name=living_situation)
        except CurrentLiving.DoesNotExist:
            return Response({"error": "Invalid living situation value"}, status=status.HTTP_400_BAD_REQUEST)

        instance.current_living = living_situation
        instance.save()

        return Response({"message": "Living situation updated successfully."}, status=status.HTTP_200_OK)
    
    
    
class UpdateMotherName(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return FamilyInformation.objects.get(user=self.request.user)  

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        mother_name = request.data.get("mother_name")

        if not mother_name:
            return Response({"error": "mother name is required"}, status=status.HTTP_400_BAD_REQUEST)

        instance.mother_name = mother_name  
        instance.save()

        return Response({"message": "mother name updated successfully."}, status=status.HTTP_200_OK)   
    
        

class MessageUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.GET.get("user_id")  
        
        if not user_id:
            return Response({"error": "User ID is required"}, status=400)

        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)

        return Response(serializer.data, status=200)
    
    
