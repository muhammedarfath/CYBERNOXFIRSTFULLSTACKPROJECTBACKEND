
from django.urls import path
from .views import *

urlpatterns = [
    path('fetch-physical-status/', FetchPhysicalStatus.as_view(), name='fetch-physical-status'),
    path('fetch-drinking-status/', FetchDrinkingStatus.as_view(), name='fetch-drinking-status'),
    path('fetch-smoking-status/', FetchSmokingStatus.as_view(), name='fetch-smoking-status'),
    path('fetch-marital-status/', FetchMaritalStatus.as_view(), name='fetch-marital-status'),
    path('update_hobbies/', UpdateUserHobbyView.as_view(), name='update_hobbies'),
    path('fetch-body-art/', FetchBodyArt.as_view(), name='fetch-body-art'),
    path('fetch-cooking-status/', FetchCookingStatus.as_view(), name='fetch-cooking-status'),
    path('fetch-eating-status/', FetchEatingStatus.as_view(), name='fetch-eating-status'),
    path('fetch-exercise-status/', FetchExerciseStatus.as_view(), name='fetch-exercise-status'),

]

