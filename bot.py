import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salon.settings')
django.setup()

from environs import Env
from telegram.ext import ApplicationBuilder
from ptb.handlers.conversation_handlers import conversation_handler

def main():
    env = Env()
    env.read_env()
    app = ApplicationBuilder().token(env.str('TG_BOT_TOKEN')).build()
    app.add_handler(conversation_handler)

    app.run_polling()


if __name__ == '__main__':
    main()
