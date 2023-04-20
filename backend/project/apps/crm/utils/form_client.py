from .coach import check_client
from ..models import Clients, FormClient, OtherData, AllTime, Location, Days, Age, GroupType, Section


def register_client(data: dict):
    if not check_client(data['phone_number']):
        Clients.objects.create(
            fullname=data['name'], phone_number=data['phone_number'],
            payed_status=Clients.NEW_CLIENT, status=Clients.NEW,
            status_coach=Clients.NOT_CHECKED, status_operator=Clients.NOT_CHECK
        ).save()
    client = check_client(data['phone_number'])
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
        if isinstance(val, Clients) or not val or not len(val) > 1:
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


def get_form_data() -> dict:
    return dict(
        time=[{"title": element.time, "value": element.id} for element in AllTime.objects.all()],
        location=[{"title": element.location, "value": element.id} for element in Location.objects.all()],
        days=[{"title": element.day, "value": element.id} for element in Days.objects.all()],
        age=[{"title": element.age, "value": element.id} for element in Age.objects.all()],
        groups_type=[{"title": element.class_type, "value": element.id} for element in GroupType.objects.all()],
        **return_section()
    )


def return_section() -> dict:
    all_section = Section.objects.all()
    return dict(
        yoga_type=[{"title": element.section, "value": element.key} for element in all_section if
                   'yoga_sec_' in element.key],
        matrial_arts_type=[{"title": element.section, "value": element.key} for element in all_section if
                           'mat_sec_' in element.key],
    )
