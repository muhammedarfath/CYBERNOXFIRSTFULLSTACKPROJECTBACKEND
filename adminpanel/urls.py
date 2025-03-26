
from django.urls import path
from .views import *

urlpatterns = [
    path('adminlogin/', AdminLogin.as_view(), name='adminlogin'),
    path('fetch-all-users/', FetchAllUsers.as_view(), name='fetch-all-users'),
    path('verifications/', UserVerificationList.as_view(), name='verification-list'),

]

