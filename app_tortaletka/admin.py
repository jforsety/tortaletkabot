import asyncio
import logging
import os
import time
from pathlib import Path

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from asgiref.sync import sync_to_async
from background_task import background
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django import forms
from dotenv import load_dotenv

from tortaletka import settings
from .models import Client, BroadcastMessage

load_dotenv()

logger = logging.getLogger(__name__)

bot_instance = Bot(token=os.getenv("TOKEN_BOT"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("external_id", "first_name", "username", "attempt", "referrals", "last_date")
    list_filter = ("first_name", "username", "attempt", "referrals")
    fields = ("first_name", "username", "attempt")


admin.site.unregister(User)
admin.site.unregister(Group)


class BroadcastMessageForm(forms.ModelForm):
    class Meta:
        model = BroadcastMessage
        fields = '__all__'
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        content_type = cleaned_data.get('content_type')
        text = cleaned_data.get('text')
        image = cleaned_data.get('image')

        if content_type in ['text', 'both'] and not text:
            raise forms.ValidationError("Текст обязателен для выбранного типа контента")

        if content_type in ['image', 'both'] and not image:
            raise forms.ValidationError("Изображение обязательно для выбранного типа контента")

        return cleaned_data


@background(schedule=5)
def send_bg_message(message_id, external_id):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def async_send():
        global bot_instance
        try:
            # Получаем сообщение
            get_message = sync_to_async(
                lambda: BroadcastMessage.objects.get(id=message_id),
                thread_sensitive=True
            )
            message = await get_message()

            if message.sent:
                return

            # Проверка получателя
            if not message.is_broadcast:
                check_recipient = sync_to_async(
                    lambda: message.users.filter(external_id=external_id).exists(),
                    thread_sensitive=True
                )
                is_recipient = await check_recipient()
                if not is_recipient:
                    return

            # Отправка контента
            if message.content_type == 'text':
                await bot_instance.send_message(external_id, message.text)
            else:
                file_path = Path(settings.MEDIA_ROOT) / message.image.name
                photo = FSInputFile(str(file_path))

                if message.content_type == 'image':
                    await bot_instance.send_photo(external_id, photo)
                else:
                    await bot_instance.send_photo(external_id, photo, caption=message.text)

            # Обновление статуса
            update_status = sync_to_async(
                lambda: BroadcastMessage.objects.filter(id=message_id).update(sent=True),
                thread_sensitive=True
            )
            await update_status()
            await asyncio.sleep(0.5)

        except Exception as e:
            logger.error(f"🚨 Error: {str(e)}", exc_info=True)
            if "retry after" in str(e).lower():
                retry_time = int(''.join(filter(str.isdigit, str(e))))
                await asyncio.sleep(retry_time + 5)

    loop.run_until_complete(async_send())
    loop.close()


@admin.register(BroadcastMessage)
class BroadcastMessageAdmin(admin.ModelAdmin):
    actions = ['send_background_action']  # Добавляем кастомное действие
    list_display = ['id', 'title', 'content_type', 'truncated_text', 'sent']

    # Метод для действия
    @admin.action(description="📨 Отправить сообщение фоном")
    def send_background_action(self, request, queryset):
        for message in queryset:
            recipients = Client.objects.all() if message.is_broadcast else message.users.all()

            # Ограничение скорости: 25 сообщений/сек
            for i, client in enumerate(recipients):
                send_bg_message(message.id, client.external_id)

                # Пауза каждые 20 сообщений
                if i % 20 == 0:
                    time.sleep(1)

        self.message_user(request, f"Сообщения поставлены в очередь! Проверьте фоновые задачи.")

    def truncated_text(self, obj):
        return obj.text[:50] + '...' if obj.text else ''

    truncated_text.short_description = 'Текст'
