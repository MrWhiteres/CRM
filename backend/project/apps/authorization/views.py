from django.http import JsonResponse
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.status import HTTP_201_CREATED

from .serializers import GoogleUserSerializer


class GoogleAuthApi(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = GoogleUserSerializer

    def post(self, request: Request, *args, **kwargs) -> JsonResponse:
        data = self.serializer_class(data=request.data)
        data.is_valid()
        print(data.validated_data)
        return JsonResponse(data=data.validated_data, status=HTTP_201_CREATED)


class GoogleRegApi(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = GoogleUserSerializer

    def post(self, request: Request, *args, **kwargs) -> JsonResponse:
        data = self.serializer_class(data=request.data)
        data.is_valid()
        print(data.validated_data)
        return JsonResponse(data=data, status=HTTP_201_CREATED)


class LoginAPI(RetrieveAPIView):
    permission_classes = (AllowAny,)


class RegistrationAPI(CreateAPIView):
    permission_classes = (AllowAny,)


class AdminAPI(RetrieveAPIView):
    permission_classes = (IsAdminUser,)
