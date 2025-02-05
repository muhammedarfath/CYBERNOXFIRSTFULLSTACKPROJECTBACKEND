
from django.urls import path
from .views import FetchDrinkingStatus, FetchPhysicalStatus,FetchSmokingStatus,FetchMaritalStatus

urlpatterns = [
    path('fetch-physical-status/', FetchPhysicalStatus.as_view(), name='fetch-physical-status'),
    path('fetch-drinking-status/', FetchDrinkingStatus.as_view(), name='fetch-drinking-status'),
    path('fetch-smoking-status/', FetchSmokingStatus.as_view(), name='fetch-smoking-status'),
    path('fetch-marital-status/', FetchMaritalStatus.as_view(), name='fetch-marital-status'),
]

