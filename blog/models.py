from django.db import models
from main_app.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Содержание')
    image = models.ImageField(upload_to='blog/', verbose_name='Изображение', **NULLABLE)
    view = models.IntegerField(default=0, verbose_name='Просмотры')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блог'
