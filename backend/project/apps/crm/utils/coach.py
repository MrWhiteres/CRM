from datetime import datetime

from django.db.models import QuerySet
from django.utils import timezone

from .operators import return_base_data
from ..models import CoachForClient, Clients, ClassAttendance, NewClientCoach, AllTime, GroupType
from ...authorization.models import User


def get_clients_for_coach(user: User) -> list:
    clients = CoachForClient.objects.filter(coach=user)
    client: CoachForClient
    return [dict(
        id=client.client.id,
        first_name=client.client.name,
        last_name=client.client.lastname,
        phone_number=client.client.phone_number,
        payed_status=change_status(client.client.payed_status),
        status=None
    ) for client in clients]


def change_status(status: str) -> str:
    for elements in Clients.PAID_STATUS:
        if status in (value := list(elements)):
            return value[-1]


def get_status_paid() -> tuple:
    return Clients.PAID_STATUS


def clear_data(data: dict) -> dict:
    element: dict
    field = ['exist', 'status']
    for element in data['clients']:
        for keys in field:
            if keys not in element:
                element[keys] = False
    return data


def mark_visit_creation(data: dict, coach: User) -> None:
    client: dict
    time_correct = timezone.now().date()
    for client in data['clients']:
        if not (correct_client := check_client(client['phone_number'])):
            correct_client = Clients.objects.create(
                name=client['first_name'], lastname=client['last_name'], phone_number=client['phone_number'],
                payed_status=return_payed_status(client['status']), status_operator=Clients.CHECKED_UPLOAD,
                status_coach=Clients.CHECKED_UPLOAD
            )
            if correct_client.payed_status == 'paid':
                correct_client.payed_date = f'{time_correct.year}-{time_correct.month}-{time_correct.day}'
            create_relationship(coach=coach, client=correct_client, visit_time=client['visit_time'],
                                group_type=client['class_type'])
            correct_client.status = correct_client.RECORDED
            correct_client.save()
        if correct_client.payed_status == correct_client.NEW_CLIENT:
            correct_client.payed_status = return_payed_status(client['status'])
        if correct_client.payed_status == 'paid':
            correct_client.payed_date = f'{time_correct.year}-{time_correct.month}-{time_correct.day}'
        correct_client.save()
        create_visit(visit=client['exist'], client=correct_client)


def create_visit(visit: bool, client: Clients):
    date_now = datetime.now().date()
    try:
        element = ClassAttendance.objects.get(date=date_now, client=client)
        element.visit = visit
        element.save()
    except ClassAttendance.DoesNotExist:
        ClassAttendance.objects.create(visit=visit, client=client).save()


def check_client(phone_number) -> Clients | bool:
    try:
        return Clients.objects.get(phone_number=phone_number)
    except Clients.DoesNotExist:
        return False


def return_payed_status(data: str) -> str:
    if data == 'first':
        return Clients.FIRST
    if data == 'full':
        return Clients.PAID
    if data == 'part':
        return Clients.PART
    if data == 'one_paid':
        return Clients.ONE_PAID
    if data == 'this_month':
        return Clients.THIS_MONTH
    return Clients.NOTPAID


def create_relationship(coach: User, client: Clients, visit_time: str, group_type: str) -> None:
    try:
        CoachForClient.objects.get(coach=coach, client=client,
                                   visit_time=visit_time,
                                   group_type=group_type)
    except CoachForClient.DoesNotExist:
        CoachForClient.objects.create(
            coach=coach, client=client,
            visit_time=visit_time,
            group_type=group_type
        ).save()


def new_clients(coach: User) -> list:
    return change_choose_data(recreate_client_data(return_clients_list(return_clients(coach))))


def change_choose_data(data: list) -> list:
    element: dict
    for element in data:
        element['visit_day'] = element['visit_day'].split(', ')
        element['visit_time'] = element['visit_time'].split(', ')
        element['location'] = element['location'].split(', ')
        element['section'] = element['section'].split(', ')
        element['class_type'] = [{'title': 'Персональные', 'value': 'single'},
                                 {'title': 'Групповые', 'value': 'group'}]

    return data


def return_clients(coach: User) -> QuerySet:
    return NewClientCoach.objects.filter(coach=coach)


def return_clients_list(data: QuerySet) -> list:
    element: NewClientCoach
    return [element.client for element in data]


def recreate_client_data(data: list) -> list:
    element: Clients
    return [dict(
        name=element.name,
        lastname=element.lastname,
        phone_number=element.phone_number,
        **return_base_data(element),
        status=element.status_coach
    ) for element in data]


def create_new_clients_coach(data: dict, coach: User):
    data = cleared_data(data)
    clients = return_query_set_clients(data['id_list'])
    delete_temporary_clients(clients, coach)
    for client in clients:
        client: Clients
        client.payed_status = Clients.NEW_CLIENT
        client.status_coach = return_correct_data(client, data, 'status')
        client.save()
        for element_time in return_correct_data(client, data, 'details'):
            create_relationship(coach=coach, client=client, visit_time=element_time,
                                group_type=return_correct_data(client, data, 'class_type'))


def return_correct_data(client: Clients, data: dict, key: str) -> str:
    for element in data['clients']:
        if element['id'] == client.id:
            try:
                return element[key]
            except KeyError:
                return [element_inner[key] for element_inner in element['details'] if key in element_inner][0]
    return [element[key] for element in data['clients'] if element['id'] == client.id][0]


def cleared_data(data: dict) -> dict:
    return dict(
        clients=[
            dict(
                id=element['id'],
                status=element['status'],
                details=element['details'],
            ) for element in data['clients']
            if len(element['details']) != 0 or element['status'] != Clients.NOT_CHECKED
        ],
        id_list=[
            element['id'] for element in data['clients'] if
            len(element['details']) != 0 or element['status'] != Clients.NOT_CHECKED
        ]
    )


def return_query_set_clients(list_id: list) -> list:
    return Clients.objects.filter(id__in=list_id)


def delete_temporary_clients(clients: list, coach: User) -> None:
    for element in get_temporary_clients(clients, coach):
        element.delete()


def get_temporary_clients(clients: list, coach: User) -> list:
    return NewClientCoach.objects.filter(coach=coach, client__in=clients)


def return_time() -> list:
    time: AllTime
    return [
        dict(
            title=time.time,
            value=time.time
        ) for time in AllTime.objects.all()
    ]


def return_class_type() -> list:
    class_type: GroupType
    return [
        dict(
            title=class_type.class_type,
            value=class_type.key
        ) for class_type in GroupType.objects.all()
    ]
