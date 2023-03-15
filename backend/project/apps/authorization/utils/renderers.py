from ..models import User


def renderer_user(*, user: User) -> dict:
    base_name = 'Users'
    base_last = "Djangos"
    base_number = "380336699888"
    return {
        'email': user.email, 'first_name': user.first_name if user.first_name else base_name,
        'last_name': user.last_name if user.last_name else base_last, 'type': user.profile.type,
        'full_name': f'{user.last_name if user.last_name else base_last}'
                     f' {user.first_name if user.first_name else base_name}',
        'image': True if user.profile.image else False,
        'phone_number': user.profile.phone_number if user.profile.phone_number else base_number
    }
