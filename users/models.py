from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    verify_code = models.CharField(max_length=30, verbose_name='Код проверки', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='Страна', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='Город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            (
                'block_user',
                'Can block user'
            )
        ]
