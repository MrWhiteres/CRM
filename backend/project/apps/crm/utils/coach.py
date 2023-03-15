from datetime import datetime

from django.db.models import QuerySet
from django.utils import timezone

from ..models import CoachForClient, Clients, WorkTime, AllTime, ClassAttendance
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
            create_relationship(coach=coach, client=correct_client, visit_time=client['visit_time'])
            correct_client.status = correct_client.RECORDED
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


def create_relationship(coach: User, client: Clients, visit_time: str) -> None:
    new_relationship = CoachForClient.objects.create(
        coach=coach, client=client,
        visit_time=return_time_element_coach(coach, visit_time)
    )
    new_relationship.save()


def return_time_element_coach(coach: User, visit_time: str) -> WorkTime:
    return WorkTime.objects.get(coach=coach, work_time=AllTime.objects.get(time=visit_time))


def return_work_time_coach(coach: User) -> list:
    work_time: QuerySet = WorkTime.objects.filter(coach=coach)
    element: WorkTime
    return [dict(title=element.work_time.time, value=element.work_time.time) for element in work_time]

