from re import sub

from django.http import QueryDict

from ..models import User


def clear_data(data: QueryDict) -> dict:
    return {delete_other_element(key): value for key, value in data.items() if value}


def delete_other_element(data: str) -> str:
    return sub(r"[\[\](){}]", '', data)


def update_user_data(data: dict, user: User) -> bool:
    flag = False
    if first_name := data.get('first_name'):
        user.first_name = first_name
        flag = True
    if last_name := data.get('last_name'):
        user.last_name = last_name
        flag = True
    if image := data.get('image'):
        if user.profile.image:
            user.profile.image.delete()
            user.profile.save()
        user.profile.image = image
        flag = True
    if phone_number := data.get('phone_number'):
        user.profile.phone_number = phone_number
        flag = True
    user.save()
    user.profile.save()
    return flag
