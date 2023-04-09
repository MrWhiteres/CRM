from ast import literal_eval

from django.db.models import QuerySet
from django.forms import model_to_dict

from ..models import Clients, FormClient, OtherData, GroupType, NewClientCoach, CoachForClient
from ...authorization.models import User, Profile


def get_all_new_clients() -> list:
    all_clients = Clients.objects.filter(status=Clients.NEW)
    return recreate_client_data(all_clients)


def recreate_client_data(data: QuerySet) -> list:
    element: Clients
    return [
        dict(
            name=element.name,
            lastname=element.lastname,
            **return_base_data(element),
            phone_number=element.phone_number,
            date_added=element.date_added,
            date_update=element.date_update,
            crm_status=element.status_operator,
            data=element.date_added,
            coach=return_coach(element)
        )
        for element in data
    ]


def return_coach(data: Clients) -> list | bool:
    try:
        element: CoachForClient
        return [f"{element.coach.last_name} {element.coach.first_name}" for element in
                CoachForClient.objects.filter(client=data)]
    except CoachForClient.DoesNotExist:
        return False


def get_operator_client_status() -> list:
    return [
        dict(
            title=list(element)[1],
            value=list(element)[0]
        ) for element in Clients.CRM_STATUS
    ]


def get_all_coach() -> list:
    element: User
    return [
        dict(
            title=f'{element.last_name} {element.first_name}',
            value=element.id
        ) for element in User.objects.filter(profile__type__in=[Profile.COACH, Profile.HEAD_COACH])
    ] + [dict(
        title='Не выбран',
        value=False
    )]


def get_group_client_status() -> list:
    return [
        dict(
            title=element.class_type,
            value=element.key
        ) for element in GroupType.objects.all()
    ]


def return_base_data(element: Clients) -> dict:
    form_data = None
    other_data = None
    try:
        form_data = FormClient.objects.get(client=element)
    except FormClient.DoesNotExist:
        pass
    try:
        other_data = OtherData.objects.get(client=element)
    except OtherData.DoesNotExist:
        pass
    data_returned = {}
    if form_data:
        form_data = return_model_to_dict(form_data)
        del form_data['client']
    if other_data:
        other_data = return_model_to_dict(other_data)
        del other_data['client']
    try:
        if other_data and form_data:
            if 'location' in other_data and 'location' in form_data:
                data_returned['location'] = other_data['location'] + form_data['location']
            else:
                data_returned['location'] = other_data['location'] if 'location' in other_data else form_data[
                    'location']

            if 'section' in other_data and 'section' in form_data:
                data_returned['section'] = other_data['section'] + form_data['section']
            else:
                data_returned['section'] = other_data['section'] if 'section' in other_data else form_data['section']

            del other_data['location']
            del form_data['location']
            del other_data['section']
            del form_data['section']
    except TypeError:
        pass
    if form_data:
        data_returned = {**data_returned, **form_data}
    if other_data:
        data_returned = {**data_returned, **other_data}
    return cleared_data(data_returned)


def cleared_data(data: dict) -> dict:
    data['location'] = ', '.join(literal_eval(data['location']))
    data['section'] = ', '.join(literal_eval(data['section']))
    data['visit_day'] = ', '.join(literal_eval(data['visit_day']))
    data['visit_time'] = ', '.join(literal_eval(data['visit_time']))
    return data


def return_model_to_dict(model) -> dict:
    return model_to_dict(model)


def add_clients_to_coach(data: dict) -> None:
    clients = data['clients']
    client: dict
    for client in clients:
        if not client['coach'] or client['crm_status'] == Clients.NOT_CHECK:
            continue
        client_object = Clients.objects.get(id=client['id'])
        client_object.status_operator = client['crm_status']
        if client_object.status_operator == Clients.CHECKED_CLOSED:
            client_object.status = Clients.REFUSAL
            client_object.save()
            continue
        client_object.status = Clients.RECORDED
        client_object.status_coach = Clients.NOT_CHECKED
        client_object.save()
        create_temporary_relationship(client_object, client['coach'])


def create_temporary_relationship(client: Clients, coach: id) -> None:
    NewClientCoach.objects.create(
        client=client,
        coach=User.objects.get(id=coach)
    ).save()


def get_all_clients() -> list:
    return recreate_client_data(get_all_clients_coach())


def get_all_clients_coach() -> QuerySet:
    return Clients.objects.all().exclude(status=Clients.NEW)
