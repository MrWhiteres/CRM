from rest_framework.fields import CharField, EmailField
from rest_framework.serializers import Serializer


class TokenUserSerializer(Serializer):
    token = CharField(required=True)


class RegistrationUserSerializer(Serializer):
    email = EmailField(required=True, min_length=5, max_length=50)
    password = CharField(required=True, min_length=8, max_length=50)
    confirm_password = CharField(required=True, min_length=8, max_length=50)
    username = CharField(required=True, min_length=5, max_length=50)


class LoginUserSerializer(Serializer):
    email = EmailField(required=True, min_length=5, max_length=50)
    password = CharField(required=True, min_length=8, max_length=50)
