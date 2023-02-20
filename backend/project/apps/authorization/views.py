from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser


class LoginAPI(RetrieveAPIView):
    permission_classes = (AllowAny,)


class RegistrationAPI(CreateAPIView):
    permission_classes = (IsAuthenticated,)


class AdminAPI(RetrieveAPIView):
    permission_classes = (IsAdminUser,)
