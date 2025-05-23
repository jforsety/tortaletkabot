from django.db import models


class Client(models.Model):
    external_id = models.PositiveIntegerField(verbose_name='ID', unique=True)
    first_name = models.CharField(max_length=30, verbose_name='Имя', null=True)
    last_name = models.CharField(max_length=30, verbose_name='Фамилия', null=True)
    username = models.CharField(max_length=30, verbose_name='nickname', null=True)
    attempt = models.IntegerField(default=10, verbose_name='Попытки')
    premium_status = models.BooleanField(default=False, verbose_name='Премиум статус')
    referrals = models.IntegerField(default=0, verbose_name='Рефералы')
    date_registration = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    last_date = models.DateTimeField(auto_now=True, verbose_name='Дата активности')

    class Meta:
        verbose_name = 'Пользователя бота'
        verbose_name_plural = 'Пользователи бота'
        ordering = ['date_registration']

    def __str__(self):
        return f'{self.id} : {self.first_name}'


class BroadcastMessage(models.Model):
    CONTENT_TYPE_CHOICES = (
        ('text', 'Только текст'),
        ('image', 'Только изображение'),
        ('both', 'Текст + изображение'),
    )

    content_type = models.CharField(
        max_length=5,
        choices=CONTENT_TYPE_CHOICES,
        default='text',
        verbose_name="Тип контента"
    )
    title = models.CharField(
        verbose_name="Тема",
        max_length=150
    )
    text = models.TextField(
        verbose_name="Текст сообщения",
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to='broadcast/',
        verbose_name="Изображение",
        null=True,
        blank=True
    )
    is_broadcast = models.BooleanField(
        default=False,
        verbose_name="Всем пользователям"
    )
    users = models.ManyToManyField(
        Client,
        blank=True,
        verbose_name="Конкретные пользователи"
    )
    sent = models.BooleanField(default=False, verbose_name="Отправлено")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'{self.id} : {self.title}'
