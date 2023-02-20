from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models import Model, EmailField, BooleanField, CASCADE, OneToOneField, DateTimeField, CharField


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""
    username = CharField(verbose_name="Юзернейм", max_length=20, db_index=True, unique=True)
    email = EmailField(verbose_name='Електронная почта', db_index=True, unique=True)
    email_verify = BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = 'Пользователь'

    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.department}'


def path_to_image_profile(instance, filename: str) -> str:
    return f'users/profile-{instance.user.username}/profile_image{filename[filename.rfind("."):]}'


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE, db_index=True)
    first_name = CharField(max_length=20, verbose_name='Имя', blank=True, null=True)
    last_name = CharField(verbose_name="Фамилия", max_length=20, blank=True, null=True)

    create_at = DateTimeField(
        verbose_name="Дата регистрации", auto_now_add=True,
        editable=False,
    )
    update_at = DateTimeField(verbose_name="Дата последнего обновления", auto_now=True)

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профиль пользователя"

    def __str__(self):
        return f'{self.user.username} / {self.first_name}-{self.last_name}'
