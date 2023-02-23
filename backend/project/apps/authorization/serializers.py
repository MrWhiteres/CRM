from rest_framework.fields import EmailField, CharField
from rest_framework.serializers import Serializer


class GoogleUserSerializer(Serializer):
    email = EmailField(required=True)
    token = CharField(required=True)
