from django.db import models


class Client(models.Model):
    external_id = models.PositiveIntegerField(verbose_name='ID', unique=True)
    first_name = models.CharField(max_length=30, verbose_name='Имя', null=True)
    last_name = models.CharField(max_length=30, verbose_name='Фамилия', null=True)
    username = models.CharField(max_length=30, verbose_name='nickname', null=True)
    attempt = models.IntegerField(default=10, verbose_name='Попытки')
    premium_status = models.BooleanField(default=0, verbose_name='Премиум статус')
    referrals = models.IntegerField(default=0, verbose_name='Рефералы')
    date_registration = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    last_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата активности')

    class Meta:
        verbose_name = 'Пользователи бота'
        verbose_name_plural = 'Пользователи бота'
        ordering = ['date_registration']