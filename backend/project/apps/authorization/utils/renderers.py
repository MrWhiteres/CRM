import base64

from PIL import Image
from django.forms import model_to_dict

from ..models import User, Profile


def serialize_image(image_path) -> dict:
    # Открываем изображение
    with open(image_path, 'rb') as f:
        image = Image.open(f)
        # Преобразуем изображение в формат base64
        image_base64 = base64.b64encode(image.tobytes()).decode('utf-8')
        # Создаем словарь с информацией об изображении
        image_info = {
            'filename': image.filename,
            'width': image.width,
            'height': image.height,
            'data': image_base64
        }
        return image_info


def renderer_user(*, user: User) -> dict:
    return {
        'email': user.email, 'first_name': user.first_name,
        'last_name': user.last_name, 'type': user.profile.type,
        'full_name': f'{user.last_name} {user.first_name}',
        'image': True if user.profile.image else False,
        'phone_number': user.profile.phone_number
    }
