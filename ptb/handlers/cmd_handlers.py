from ptb.keyboards.keyboard import main_menu
from . import states_bot


async def start(update, context):
    await update.message.reply_text(
        'Главное меню',
        reply_markup=main_menu()
    )

    return states_bot.MAIN_MENU
