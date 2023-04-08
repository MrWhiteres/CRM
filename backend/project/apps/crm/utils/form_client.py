from .coach import check_client
from ..models import Clients, FormClient, OtherData


def register_client(data: dict):
    create_form_client(data)


def create_form_client(data: dict):

    if not check_client(data['phone_number']):
        Clients.objects.create(
            name=data['name'], phone_number=data['phone_number'],
            payed_status=Clients.NEW_CLIENT, status=Clients.NEW,
            status_coach=Clients.NOT_RECORDED, status_operator=Clients.NOT_CHECK
        ).save()

    client = Clients.objects.get(phone_number=data['phone_number'])

    data_base: dict = dict(client=client)
    data_other: dict = dict(client=client)

    if loc := data.get('training_location'):
        data_base['location'] = str(loc)
    if loc := data.get('other_location'):
        data_other['location'] = str(loc)

    data_base['visit_time'] = str(data['training_time'])

    if sec := data.get('matrial_arts_type') or (sec_2 := data.get('yoga_type')):
        data_base['section'] = str(sec) or str(sec_2)
    if sec := data.get('other_matrial_arts_type') or (sec_2 := data.get('other_yoga_type')):
        data_other['section'] = str(sec) or str(sec_2)

    data_base['age'] = data['age']
    data_base['visit_day'] = str(data['visit_day'])
    data_base['class_type'] = str(data['class_type'])

    dict_filter(data_base, FormClient)
    dict_filter(data_other, OtherData)


def dict_filter(dict_obj: dict, model: FormClient or OtherData) -> None:
    for val in dict_obj.values():
        if isinstance(val, Clients) or not len(val) > 1:
            continue
        return create_form(model, dict_obj)
    return None


def create_form(model: FormClient or OtherData, data: dict):
    model.objects.create(**data).save()


def clean_data(data: dict) -> dict:
    data: dict = data['data']
    delete_key = [key for key, value in data.items() if not value]
    for key in delete_key:
        del data[key]
    return data
