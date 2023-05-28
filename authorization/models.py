import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Создает и сохраняет обычного пользователя с заданными данными.

        Args:
            username (str): Имя пользователя.
            email (str): Адрес электронной почты пользователя.
            password (str, optional): Пароль пользователя. Defaults to None.

        Returns:
            User: Созданный пользователь.
        """
        if not email:
            raise ValueError('Email is required')
        if not username:
            raise ValueError('Username is required')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Создает и сохраняет суперпользователя с заданными данными.

        Args:
            username (str): Имя пользователя.
            email (str): Адрес электронной почты пользователя.
            password (str): Пароль пользователя.

        Returns:
            User: Созданный суперпользователь.
        """
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    subscriptions = models.ManyToManyField('self', blank=True, related_name='subscribers', symmetrical=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    @property
    def token(self):
        """
        Возвращает JWT-токен пользователя.

        Returns:
            str: JWT-токен пользователя.
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        Возвращает полное имя пользователя.

        Returns:
            str: Полное имя пользователя.
        """
        return self.username

    def get_short_name(self):
        """
        Возвращает сокращенное имя пользователя.

        Returns:
            str: Сокращенное имя пользователя.
        """
        return self.username

    def _generate_jwt_token(self):
        """
        Генерирует JWT-токен для пользователя.

        Returns:
            str: Сгенерированный JWT-токен.
        """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token

