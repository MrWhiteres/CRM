from django.urls import path
from .views import GoogleRegApi, GoogleAuthApi

urlpatterns = [
    path('google/registration/', GoogleRegApi.as_view()),
    path('google/login/', GoogleAuthApi.as_view())
]
