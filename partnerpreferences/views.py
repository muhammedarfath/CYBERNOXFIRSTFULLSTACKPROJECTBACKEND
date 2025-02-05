from django.shortcuts import render
from authentication.models import DrinkingPreference, MaritalStatus, PhysicalStatus, SmokingPreference
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
    
    
    