from django.core.management.base import BaseCommand
from telegram.ext import ApplicationBuilder
from ptb.handlers.conversation_handlers import conversation_handler
from django.conf import settings
import django
import os


class Command(BaseCommand):
    help = 'Запуск Telegram бота'

    def handle(self, *args, **options):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salon.settings')
        django.setup()
        tg_bot_token = settings.TG_BOT_TOKEN
        app = ApplicationBuilder().token(tg_bot_token).build()
        app.add_handler(conversation_handler)

        self.stdout.write(self.style.SUCCESS('Бот запустился'))
        app.run_polling()
        self.stdout.write(self.style.ERROR('Бот остановлен'))
