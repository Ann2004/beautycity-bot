from . import states_bot
from ptb.keyboards import keyboard


async def handler_main_menu(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'select_salon':
        await query.message.edit_text(
            text='Выберите салон',
            reply_markup=keyboard.salon_menu()
        )
        return states_bot.SELECT_SALON

    elif query.data == 'select_master':
        await query.message.edit_text(
            text='Мастер, дата работы и салон',
            reply_markup=keyboard.master_menu()
        )
        return states_bot.SELECT_MASTER


async def handler_salon_menu(update, context):
    query = update.callback_query
    await query.answer()

    if query.data.startswith('salon_'):
        await query.message.edit_text(
            'Выберите процедуру',
            reply_markup=keyboard.procedure_menu()
        )
        return states_bot.SELECT_PROCEDURE

    elif query.data == 'back_to_main':
        await query.message.edit_text(
            'Главное меню',
            reply_markup=keyboard.main_menu()
        )
        return states_bot.MAIN_MENU


async def handler_procedure_menu(update, context):
    query = update.callback_query
    await query.answer()

    if query.data.startswith('procedure_'):
        await query.message.edit_text(
            'Выберите дату',
            reply_markup=keyboard.date_menu()
        )
        return states_bot.SELECT_DATE

    elif query.data == 'back_to_salon':
        await query.message.edit_text(
            'Выберите салон',
            reply_markup=keyboard.salon_menu()
        )
        return states_bot.SELECT_SALON


async def handler_date_menu(update, context):
    query = update.callback_query
    await query.answer()

    if query.data.startswith('date_'):
        await query.message.edit_text(
            'Выберите время',
            reply_markup=keyboard.time_menu()
        )
        return states_bot.SELECT_TIME

    elif query.data == 'back_to_procedure':
        await query.message.edit_text(
            'Выберите дату',
            reply_markup=keyboard.procedure_menu()
        )
        return states_bot.SELECT_PROCEDURE


async def handler_time_menu(update, context):
    query = update.callback_query
    await query.answer()

    if query.data.startswith('time_'):
        await query.message.edit_text(
            'Введите фио',
            reply_markup=None
        )
        return states_bot.CLIENT_NAME

    elif query.data == 'back_to_date':
        await query.message.edit_text(
            'Выберите время',
            reply_markup=keyboard.date_menu()
        )
        return states_bot.SELECT_DATE


async def handler_name_menu(update, context):
    await update.message.reply_text('Введите номер телефона')
    return states_bot.CLIENT_PHONENUMBER


async def handler_phone_menu(update, context):
    await update.message.reply_text(
        'Введите промокод',
        reply_markup=keyboard.promocode_menu()
    )
    return states_bot.PROMO


async def handler_promo_menu(update, context):
    if update.callback_query and update.callback_query.data == 'skip_promo':
        query = update.callback_query
        await query.answer()

        await query.message.edit_text(
            'Информация выбора клиента без промокода',
            reply_markup=keyboard.appointment_menu()
        )
        return states_bot.APPOINTMENT

    elif update.message and update.message.text:
        await update.message.reply_text(
            'Информация выбора клиента с промокодом',
            reply_markup=keyboard.appointment_menu()
        )
        return states_bot.APPOINTMENT


async def handler_appointment_menu(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'confirm_appointment':
        await query.message.edit_text(
            'Запись подтверждена',
            reply_markup=keyboard.back_to_main_menu()
        )
        return states_bot.AFTER_APPOINTMENT

    elif query.data == 'cancel_appointment':
        await query.message.edit_text(
            'Запись отменена',
            reply_markup=keyboard.back_to_main_menu()
        )
        return states_bot.AFTER_APPOINTMENT


async def handler_after_appointment(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'back_to_main':
        await query.message.edit_text(
            'Главное меню',
            reply_markup=keyboard.main_menu()
        )
        return states_bot.MAIN_MENU


async def handler_master_menu(update, context):
    query = update.callback_query
    await query.answer()

    if query.data.startswith('master_'):
        await query.message.edit_text(
            'Выберите процедуру',
            reply_markup=keyboard.procedure_menu()
        )
        return states_bot.SELECT_PROCEDURE

    elif query.data == 'back_to_main':
        await query.message.edit_text(
            'Главное меню',
            reply_markup=keyboard.main_menu()
        )
        return states_bot.MAIN_MENU
