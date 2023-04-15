from ..models import User


def renderer_user(*, user: User) -> dict:
    return {
        'email': user.email, 'first_name': user.first_name,
        'last_name': user.last_name, 'type': user.user_type,
        'full_name': f'{user.last_name} {user.first_name}',
        'image': True if user.image else False,
        'phone_number': user.phone_number
    }
