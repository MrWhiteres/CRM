from rest_framework.fields import ListField, CharField
from rest_framework.serializers import Serializer


class ClientsSerializer(Serializer):
    clients = ListField(required=True)


class FormSerializer(Serializer):
    name = CharField(required=True, min_length=3)
    phone_number = CharField(required=True, min_length=10)
    choice = CharField(required=True, min_length=4)
    class_type = CharField(required=True, min_length=1)
    training_location = ListField(required=False)
    other_location = CharField(required=False)
    training_time = ListField(required=True)
    visit_day = ListField(required=True)
    yoga_type = ListField(required=False)
    other_yoga_type = CharField(required=False)
    age = CharField(required=True)
    matrial_arts_type = ListField(required=False)
    other_matrial_arts_type = CharField(required=False)


class OperatorCrmClientsSerializer(Serializer):
    clients = ListField(required=True, min_length=1)


