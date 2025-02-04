import asyncio

from django.core.management.base import BaseCommand

from app_bot.main import bot, dp, logger


class Command(BaseCommand):
    help = "Запуск телеграм бота"

    def handle(self, *args, **options):
        logger.info("Бот был запущен")
        asyncio.run(dp.start_polling(bot))
        logger.info("Бот был остановлен")

