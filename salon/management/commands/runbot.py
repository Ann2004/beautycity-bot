from django.core.management.base import BaseCommand
from telegram.ext import ApplicationBuilder
from ptb.handlers import conversation_handlers
from salon.workers.repeat_offer import repeat_offer_worker
from django.conf import settings
import django
import os
import asyncio


class Command(BaseCommand):
    help = 'Запуск Telegram бота'

    def handle(self, *args, **options):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salon.settings')
        django.setup()

        tg_bot_token = settings.TG_BOT_TOKEN

        async def post_init(app):
            # Запускаем воркер
            asyncio.create_task(repeat_offer_worker(app.bot))
            print('repeat_offer_worker запущен')

        app = (
            ApplicationBuilder()
            .token(tg_bot_token)
            .post_init(post_init)
            .build()
        )

        app.add_handler(conversation_handlers.conversation_handler)

        self.stdout.write(self.style.SUCCESS('Бот запущен'))
        app.run_polling()
        self.stdout.write(self.style.ERROR('Бот остановлен'))