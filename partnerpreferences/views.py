from django.shortcuts import render
from .serializers import BodyArtStatusSerializer, CookingSkillStatusSerializer, EatingStatusSerializer, ExerciseStatusSerializer, UserHobbySerializer
from .models import BodyArt, CookingSkill, EatingHabit, Exercise, PartnerExpectation, UserHobby
from authentication.models import AnnualIncome, DrinkingPreference, Education, Employment, MaritalStatus, PhysicalStatus, SmokingPreference
from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.serializers import DrinkingStatusSerializer, PhysicalStatusSerializer,SmokingStatusSerializer,MaritalStatusSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
# Create your views here.


class FetchPhysicalStatus(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        physical_statuses = PhysicalStatus.objects.all()  
        serializer = PhysicalStatusSerializer(physical_statuses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FetchDrinkingStatus(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        physical_statuses = DrinkingPreference.objects.all()  
        serializer = DrinkingStatusSerializer(physical_statuses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    
  
class FetchSmokingStatus(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        physical_statuses = SmokingPreference.objects.all()  
        serializer = SmokingStatusSerializer(physical_statuses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  


class FetchMaritalStatus(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        physical_statuses = MaritalStatus.objects.all()  
        serializer = MaritalStatusSerializer(physical_statuses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  
    
class UpdatePartnerExpectation(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
        
        # Get or create the partner expectation object for the current user
        partner_expectation, created = PartnerExpectation.objects.get_or_create(user=user)

        # Update simple fields
        if 'age_preference' in data:
            partner_expectation.age_preference = data['age_preference']
        
        if 'height_preference' in data:
            partner_expectation.height_preference = data['height_preference']
        
        if 'mother_tongue' in data:
            partner_expectation.mother_tongue = data['mother_tongue']
        
        if 'partner_district' in data:
            partner_expectation.partner_district = data['partner_district']
        
        if 'partner_country' in data:
            partner_expectation.partner_country = data['partner_country']

        def update_many_to_many_field(field_name, model):
            if field_name in data:
                ids = data.get(field_name, [])  # Get IDs list from request
                instances = model.objects.filter(id__in=ids)  # Get existing records
                getattr(partner_expectation, field_name).set(instances)  # Update field

        # Updating ManyToMany Fields
        update_many_to_many_field('marital_status', MaritalStatus)
        update_many_to_many_field('physical_status', PhysicalStatus)
        update_many_to_many_field('drinking_preference', DrinkingPreference)
        update_many_to_many_field('smoking_preference', SmokingPreference)
        update_many_to_many_field('education', Education)
        update_many_to_many_field('profession', Employment)
        update_many_to_many_field('annual_income', AnnualIncome)

        # Save the updated partner expectation
        partner_expectation.save()

        return Response({'message': 'Partner expectation updated successfully'}, status=status.HTTP_200_OK) 
    
              
class UpdateUserHobbyView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = request.user
        try:
            user_hobby, created = UserHobby.objects.get_or_create(user=user)

            serializer = UserHobbySerializer(user_hobby, data=request.data, partial=True)
                        
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Hobbies updated successfully", "data": serializer.data},
                    status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FetchBodyArt(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        body_statuses = BodyArt.objects.all()  
        serializer = BodyArtStatusSerializer(body_statuses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)   
    
    
class FetchCookingStatus(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        cooking_statuses = CookingSkill.objects.all()  
        serializer = CookingSkillStatusSerializer(cooking_statuses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)   
    
class FetchEatingStatus(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        eating_statuses = EatingHabit.objects.all()  
        serializer = EatingStatusSerializer(eating_statuses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)   
    
class FetchExerciseStatus(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        eating_statuses = Exercise.objects.all()  
        serializer = ExerciseStatusSerializer(eating_statuses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)     
    
    
    
