from django.urls import path
from .views import *
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("reset-password/<uidb64>/<token>/", ResetPasswordView.as_view(), name="reset-password"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('get-gender/', GenderView.as_view(), name='get-gender'),
    path('get-create-for/', CreateForView.as_view(), name='get-create-for'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('check-user-details/', CheckBasicDetailsView.as_view(), name='check_user_details'),
    path('profile-groom-bride-family-create/', ProfileGroomBrideFamilyCreateView.as_view(), name='profile-groom-bride-family-create'),
    path('religions/', ReligionListView.as_view(), name='religion-list'),
    path('castes/<int:religion_id>/', CasteListView.as_view(), name='caste-list'),
    path('marital/', MaritalListView.as_view(), name='marital-list'),
    path('bodytype/', BodyListView.as_view(), name='body_type'),
    path('educations/', EducationListView.as_view(), name='educations'),
    path('employements/', EmployementsListView.as_view(), name='employements'),
    path('occupations/', OccupationListView.as_view(), name='occupations'),
    path('annualincome/', AnnualIncomeListView.as_view(), name='annualincome'),
    path('familytype/', FamilyTypeListView.as_view(), name='familytype'),
    path('familystatus/', FamilyStatusListView.as_view(), name='familystatus'),
    path('fetch-profile-details/', FetchProfileDetails.as_view(), name='fetch-profile-details'),
    path('posts/', PostCreateAPIView.as_view(), name='post-create'),
    path('posts/<int:post_id>/', PostDeleteAPIView.as_view(), name='delete-post'),
    path('update-profile/', UserProfileUpdateView.as_view(), name='update-profile'),
    path('fetch-users/', FetchUsers.as_view(), name='fetch-users'),
    path("update-languages/", UpdateLanguagesView.as_view(), name="update-languages"),
    path("update-present-location/", UpdateLocationView.as_view(), name="update-present-location"),
    path("update-secondary-number/", UpdateSecondaryView.as_view(), name="update-secondary-number"),
    path("update-time-to-call/", UpdateTimeToCallView.as_view(), name="update-time-to-call"),
    path("update-full-address/", UpdateFullAddressView.as_view(), name="update-full-address"),
    path("update-company-name/", UpdateCompany.as_view(), name="update-company-name"),
    path("update-experience/", UpdateExperience.as_view(), name="update-experience"),
    path("fetch-reliousnes/", FetchReligiousness.as_view(), name="fetch-reliousnes"),
    path("fetch-religious-services/", FetchReligiousnesServices.as_view(), name="fetch-religious-services"),
    path("update-religiousness/", UpdateReligiousness.as_view(), name="update-religiousness"),
    path("update-religiousnes-services/", UpdateReligiousnesServices.as_view(), name="update-religiousnes-services"),
    path("fetch-polygamy/", FetchPolygamyOptions.as_view(), name="fetch-polygamy"),
    path("update-polygamy/", UpdatePolygamyPreference.as_view(), name="update-polygamy"),
    path("fetch-political/", FetchPoliticalViewOptions.as_view(), name="fetch-political"),
    path("update-political/", UpdatePoliticalViewPreference.as_view(), name="update-political"),
    path("fetch-skin-color/", FetchSkinColorOptions.as_view(), name="fetch-skin-color"),
    path("update-skin-color/", UpdateSkinColorPreference.as_view(), name="update-skin-color"),
    path("fetch-blood-group/", FetchBloodGroupOptions.as_view(), name="fetch-blood-group"),
    path("update-blood-group/", UpdateBloodGroupPreference.as_view(), name="update-blood-group"),
    path("fetch-hair-color/", FetchHairColorOptions.as_view(), name="fetch-hair-color"),
    path("update-hair-color/", UpdateHairColorPreference.as_view(), name="update-hair-color"),
    path("fetch-hair-type/", FetchHairTypeOptions.as_view(), name="fetch-hair-type"),
    path("update-hair-type/", UpdateHairTypePreference.as_view(), name="update-hair-type"),
    path("update-appearance/", UpdateAppearance.as_view(), name="update-appearance"),
    path("fetch-home-type/", FetchHomeTypeOptions.as_view(), name="fetch-home-type"),
    path("update-home-type/", UpdateHomeTypePreference.as_view(), name="update-home-type"),
    path("fetch-living-situation/", FetchLivingSituationOptions.as_view(), name="fetch-living-situation"),
    path("update-living-situation/", UpdateLivingSituationPreference.as_view(), name="update-living-situation"),
    path("update-mothername/", UpdateMotherName.as_view(), name="update-mothername"),
    path("message-user/", MessageUser.as_view(), name="message-user"),
    path("search/", Search.as_view(), name="search"),
    path("expectation/", Expectation.as_view(), name="expectation"),
    path('save-profile/', SavedProfileViewSet.as_view(), name='save-profile'),
    path('mark-as-read/<int:notification_id>/', MarkNotificationAsReadView.as_view(), name='mark-notification-as-read'),

    path('block-user/', BlockUser.as_view(), name='block_user'),
    path('unblock-user/', UnBlockUser.as_view(), name='unblock_user'),
]
