import asyncio

from django.core.management.base import BaseCommand

from app_bot.main import bot, dp, scheduler


class Command(BaseCommand):
    help = "Запуск телеграм бота"

    def handle(self, *args, **options):
        # Запуск асинхронного контекста с ботом и планировщиком
        async def main():
            # Запуск планировщика
            scheduler.start()

            # Запуск бота
            await dp.start_polling(bot)

            # Бесконечный цикл для работы планировщика
            while True:
                await asyncio.sleep(3600)  # Просто поддерживаем цикл

        asyncio.run(main())
