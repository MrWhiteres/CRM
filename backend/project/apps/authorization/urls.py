from django.urls import path
from .views import LoginUserAPI, RegistrationUserAPI, ConfirmAPI, TestApi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('registration/', RegistrationUserAPI.as_view()),
    path('login/', LoginUserAPI.as_view()),
    path('confirm/', ConfirmAPI.as_view()),
    path('get_token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('test/', TestApi.as_view(), name='test')
]
