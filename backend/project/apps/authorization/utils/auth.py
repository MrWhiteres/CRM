from re import match

from django.core.mail import send_mail
from django.template.loader import render_to_string
from requests import get
from rest_framework_simplejwt.tokens import RefreshToken

from . import pattern_dict
from ..models import User, Profile
from ....settings.config_data import URL_FRONTEND


def send_confirm_email(user: User) -> bool:
    token = user.generate_confirmation_token()
    confirm_link = f'{URL_FRONTEND}{token}'
    subject = 'Подтверждение электронной почты'
    message = f'Добро пожаловать к нам на сайт, {user.username}!'
    html_template = render_to_string(
        'mail.html', {
            'title': subject,
            'greeting': subject,
            'message': message,
            'domain_name': 'MIX Fighter',
            'link': confirm_link
        }
    )
    send_mail('Подтверждение электронной почты', message,
              'noreply@example.com', [user.email], html_message=html_template)
    return True


def confirm_user(token: str) -> bool:
    user = User.get_by_confirmation_token(token)
    if not user:
        return False
    user.confirm_registration(token)
    return True


def login_user(data: dict) -> dict:
    token = data.get('token')
    if token:
        data = get_user_data(data['token'])
    if not (user := get_user(data['email'])):
        return {'error': 'UserDoesNotExist'}
    if not user.is_active or not user.email_verify:
        return {'error': 'UserInactive'}
    if token:
        data['password'] = generate_user_password(data)
    if not user.check_password(data['password']):
        return {'error': 'InvalidPassword'}
    return get_tokens_for_user(user)


def registration_user(data: dict) -> dict or bool:
    token = data.get('token')
    if token:
        data = get_user_data(data['token'])
    if error_message := check_user(data['email'], 'email'):
        return {'error': error_message}
    if error_message := check_user(data.get('username', data.get('given_name')), 'username'):
        return {'error': error_message}
    if not (error_message := validate_password(data)):
        return {'error': error_message}
    user = User.objects.create_user(**generate_user_data(data=data, token=True)) if token \
        else User.objects.create_user(**generate_user_data(data=data))
    profile = Profile.objects.create(user=user)
    profile.save()
    return send_confirm_email(user)


def get_user_data(token: str) -> dict:
    return get(f'https://www.googleapis.com/oauth2/v3/userinfo?access_token={token}').json()


def validate_password(data: dict) -> bool:
    if not data.get('password'):
        return True
    password_validate = data['password'] == data['confirm_password'] and match(pattern_dict['password'],
                                                                               data['password'])
    return password_validate if password_validate else 'InvalidPassword'


def check_user(data: str, key: str) -> str or bool:
    try:
        User.objects.get(email=data) if key == 'email' else User.objects.get(username=data)
        return 'UserExist'
    except User.DoesNotExist:
        return False


def get_user(email: str) -> User or bool:
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return False


def generate_user_password(data: dict) -> str:
    full_name = data['name']
    google_id = data['sub']
    return f'{full_name[:3]}?{google_id[:5]}@{google_id[-6:-1]}'


def generate_user_data(data: dict, token: bool = False) -> dict:
    if not token:
        del data['confirm_password']
        return data
    return {
        'username': data['given_name'],
        'email': data['email'],
        'password': generate_user_password(data)
    }


def get_tokens_for_user(user: User) -> dict:
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
