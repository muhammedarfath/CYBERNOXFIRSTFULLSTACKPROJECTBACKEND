
from django.urls import path
from .views import *

urlpatterns = [
    path('adminlogin/', AdminLogin.as_view(), name='adminlogin'),
    path('fetch-all-users/', FetchAllUsers.as_view(), name='fetch-all-users'),
    path('verifications/', UserVerificationList.as_view(), name='verification-list'),
    path('verify-proof/<int:user_id>/', UserProofVerification.as_view(), name='verify-proof'),
    path('fetch-employees/', FetchEmployees.as_view(), name='fetch-employees'),
    path('update-employees/<int:pk>/', UpdateEmployeeRole.as_view(), name='update-employees'),
    path('create-employee/', CreateEmployee.as_view(), name='create-employee'),

]

