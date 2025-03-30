from django.core.management.base import BaseCommand
from django.core.management import call_command
import time
import traceback


class Command(BaseCommand):
    help = 'Запускает процесс задач с перезапуском при ошибках'

    def handle(self, *args, **options):
        while True:
            try:
                call_command('process_tasks')
            except Exception as e:
                self.stdout.write(f"Ошибка: {e}\n{traceback.format_exc()}")
            time.sleep(5)  # Пауза перед перезапуском