from django.urls import path

from .views import (
    CoachClients, NewClientsWithFormsAPI, AdminAndOperatorForm
)

urlpatterns = [
    path('clients-date/', CoachClients.as_view()),
    path('forms/', NewClientsWithFormsAPI.as_view()),
    path('client-list/', AdminAndOperatorForm.as_view())
]
