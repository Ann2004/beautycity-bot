from ptb.keyboards.keyboard import main_menu
from . import states_bot


async def start(update, context):
    context.user_data.clear()  # отчистка контекста на старте

    text = (
        'Вас приветствует бот салонов красоты BeautyCity\n\n'
        'Вы можете выбрать салон, мастера и оставить отзыв\n\n'
        'Если у вас возникли трудности или вам нужна консультация:\n'
        'Телефон для связи с нами: +79801234567'
    )
    await update.message.reply_text(
        text=text,
        reply_markup=main_menu()
    )

    return states_bot.MAIN_MENU
