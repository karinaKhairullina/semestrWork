from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='avatar/', blank=True)


class UserInfo(models.Model):
    user = models.ForeignKey(User, related_name='user_info', verbose_name='пользователь', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='имя')
    bio = models.TextField(verbose_name='о себе')
    avatar = models.ImageField(null=True, blank=True, upload_to='image_user_avatars', verbose_name='аватар')

    class Meta:
        verbose_name_plural = 'Информация о пользователях'
        verbose_name = 'Информация о пользователе'
