from django.http import JsonResponse
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK

from .permissions import HeightRank, AdminOperator
from .serializers import (
    ClientsSerializer, FormSerializer, OperatorCrmClientsSerializer
)
from .utils.coach import get_clients_for_coach, get_status_paid, clear_data, mark_visit_creation, return_work_time_coach
from .utils.form_client import register_client, clean_data
from .utils.operators import get_all_new_clients, get_operator_client_status, get_group_client_status, get_all_coach, \
    add_clients_to_coach


class CoachClients(RetrieveUpdateDestroyAPIView, CreateAPIView):
    permission_classes = (HeightRank,)
    serializer_class = [ClientsSerializer]

    def serializers_data(self, data: dict) -> dict or bool:
        for serializer in self.serializer_class:
            serializer_data = serializer(data=data)
            if serializer_data.is_valid():
                return {**serializer_data.validated_data}
        return False

    def get(self, request, *args, **kwargs) -> JsonResponse:
        data = get_clients_for_coach(request.user)
        status = get_status_paid()
        work_time = return_work_time_coach(request.user)
        return JsonResponse(data=dict(clients=data, status_paid=status, time=work_time), status=HTTP_200_OK)

    def post(self, request, *args, **kwargs) -> JsonResponse:
        data = self.serializers_data(request.data)
        mark_visit_creation(clear_data(data), request.user)
        return JsonResponse(data={}, status=HTTP_200_OK)


class NewClientsWithFormsAPI(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = [FormSerializer]

    def serializer_data(self, data: dict) -> dict | bool:
        for serializer in self.serializer_class:
            new_data = serializer(data=data)
            if new_data.is_valid():
                return {**new_data.validated_data}
            print(new_data.errors)
        return False

    def post(self, request, *args, **kwargs) -> JsonResponse:
        register_client(self.serializer_data(clean_data(request.data)))
        return JsonResponse(data=request.data, status=HTTP_200_OK)


class AdminAndOperatorForm(CreateAPIView, RetrieveAPIView):
    permission_classes = [AdminOperator]
    serializer_class = [OperatorCrmClientsSerializer]

    def get_object(self, data: dict) -> dict | bool:
        for serializer in self.serializer_class:
            serialize_data = serializer(data=data)
            if serialize_data.is_valid():
                return {**serialize_data.validated_data}
        return False

    def post(self, request, *args, **kwargs) -> JsonResponse:
        add_clients_to_coach(self.get_object(request.data))
        return JsonResponse(data={}, status=HTTP_200_OK)

    def get(self, request, *args, **kwargs) -> JsonResponse:
        return JsonResponse(data={'elements': get_all_new_clients(), 'crm_status': get_operator_client_status(),
                                  'group_type': get_group_client_status(), 'coach': get_all_coach()},
                            status=HTTP_200_OK)