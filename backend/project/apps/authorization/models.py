from secrets import token_urlsafe

from django.contrib.auth.models import AbstractUser, BaseUserManager, User
from django.db.models import (
    Model, EmailField, BooleanField, CASCADE,
    OneToOneField, DateTimeField, CharField, ForeignKey,
    DO_NOTHING
)
from django_resized import ResizedImageField


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields) -> User:
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields) -> User:
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields) -> User:
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = EmailField(verbose_name='Електронная почта',
                       db_index=True, unique=True)
    email_verify = BooleanField(default=False)
    is_active = BooleanField(default=False, verbose_name='Активный')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = 'Пользователь'

    objects = UserManager()

    def __str__(self) -> str:
        return f'{self.email} {self.first_name} {self.last_name}'

    def get_profile(self) -> Model:
        return Profile.objects.get(user=self)

    def generate_confirmation_token(self) -> str:
        token = EmailActivateToken.objects.create(
            user=self, confirmation_token=token_urlsafe())
        token.save()
        return token.confirmation_token

    @staticmethod
    def get_by_confirmation_token(token) -> User or None:
        try:
            user = EmailActivateToken.objects.get(
                confirmation_token=token).user
            return user
        except EmailActivateToken.DoesNotExist:
            return None

    def confirm_registration(self, token) -> None:
        self.email_verify = True
        self.is_active = True
        EmailActivateToken.objects.get(confirmation_token=token).delete()
        self.save()


def path_to_image_profile(instance, filename: str) -> str:
    return f'users/profile-{instance.user.email}/profile_image{filename[filename.rfind("."):]}'


class Profile(Model):
    ADMIN = 'admin'
    USER = 'user'
    COACH = 'coach'
    HEAD_COACH = 'head_coach'
    OPERATOR = 'operator'

    USER_STATUS = (
        (ADMIN, 'Администратор'),
        (USER, 'Юзер'),
        (COACH, 'Тренер'),
        (HEAD_COACH, 'Старший тренер'),
        (OPERATOR, 'Оператор'),
    )

    YOGA = 'yoga'
    MARTIALARTS = 'martialArts'
    SECTION = (
        (YOGA, 'йога'),
        (MARTIALARTS, "единоборства")
    )
    user = OneToOneField(User, on_delete=CASCADE, db_index=True)
    type_section = CharField(verbose_name='Тип секции', max_length=255, choices=SECTION, default=None, blank=True,
                             null=True)
    type = CharField(
        verbose_name="Тип профиля",
        choices=USER_STATUS,
        default=USER,
        max_length=20, )
    create_at = DateTimeField(
        verbose_name="Дата регистрации", auto_now_add=True,
        editable=False,
    )
    update_at = DateTimeField(
        verbose_name="Дата последнего обновления", auto_now=True)
    image = ResizedImageField(verbose_name='Изображение профиля', force_format="WEBP", quality=100,
                              upload_to=path_to_image_profile, blank=True, null=True)
    phone_number = CharField(
        verbose_name='Номер телефона', blank=True, null=True, max_length=255)

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профиль пользователя"

    def __str__(self) -> str:
        return f'Profile - {self.user}'


class EmailActivateToken(Model):
    user = ForeignKey(User, on_delete=DO_NOTHING)
    confirmation_token = CharField(
        verbose_name='Токен', null=True, blank=True, max_length=255)


class TypeSection(Model):
    section_type = CharField(verbose_name='Направление секции', max_length=255)


class SectionYoga(Model):
    yoga = ()
    type_section = ForeignKey(TypeSection, verbose_name='Направление', on_delete=DO_NOTHING)
    sub_type_section = CharField(verbose_name='Тип секции', max_length=255)


class SectionFighter(Model):
    fighter = ()
    type_section = ForeignKey(TypeSection, verbose_name='Направление', on_delete=DO_NOTHING)
    sub_type_section = CharField(verbose_name='Тип секции', max_length=255)
