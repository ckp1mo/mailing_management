from datetime import time
from django.conf import settings
from django.db import models
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(max_length=150, verbose_name='email')
    name = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.CharField(max_length=200, verbose_name='комментарий', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', **NULLABLE)

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name='Тема')
    body = models.TextField(**NULLABLE, verbose_name='содержание')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', **NULLABLE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'


class Mailing(models.Model):
    daily = 'Раз в день'
    weekly = 'Раз в неделю'
    monthly = 'Раз в месяц'

    frequency_choices = [
        (daily, 'Раз в день'),
        (weekly, 'Раз в неделю'),
        (monthly, 'Раз в месяц'),
    ]

    created = 'Создана'
    started = 'Запущена'
    completed = 'Завершена'
    status_choices = [
        (created, 'Создана'),
        (started, 'Запущена'),
        (completed, 'Завершена'),
    ]

    start_time = models.TimeField(default=time(hour=12), verbose_name='Время начала рассылки')
    end_time = models.TimeField(default=time(hour=16), verbose_name='Время окончания рассылки')
    frequency = models.CharField(max_length=50, default=daily, choices=frequency_choices,
                                 verbose_name='Частота отправки')
    status = models.CharField(max_length=50, choices=status_choices, default=created, verbose_name='Статус')
    clients = models.ManyToManyField(Client, verbose_name='клиенты рассылки')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')

    def __str__(self):
        return f"{self.start_time} - {self.end_time}, {self.frequency}, {self.status}, Активна: {self.is_active}"

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'


class Log(models.Model):
    time = models.DateTimeField(auto_now_add=True, verbose_name='Дата последней отправки')
    status = models.CharField(max_length=30, verbose_name='статус рассылки')
    server_response = models.CharField(**NULLABLE, verbose_name='ответ сервера')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка', **NULLABLE)
    client = models.CharField(max_length=100, verbose_name='Клиент', **NULLABLE)

    def __str__(self):
        return f"{self.owner}, {self.status}"

    class Meta:
        verbose_name = 'логи'
        verbose_name_plural = 'логи'
