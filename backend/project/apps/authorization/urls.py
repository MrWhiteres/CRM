from django.urls import path
from .views import (
    LoginUserAPI, RegistrationUserAPI, ConfirmAPI,
    UserDataApi, ImageAPI)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('registration/', RegistrationUserAPI.as_view()),
    path('login/', LoginUserAPI.as_view()),
    path('confirm/', ConfirmAPI.as_view()),
    path('get_token/', TokenObtainPairView.as_view()),
    path('refresh_token/', TokenRefreshView.as_view()),
    path('user/profile/', UserDataApi.as_view()),
    path('user/image/', ImageAPI.as_view())
]
