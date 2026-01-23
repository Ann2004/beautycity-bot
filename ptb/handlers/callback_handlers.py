from . import states_bot
from ptb.keyboards import keyboard

from salon.services import ( 
    get_or_create_client, create_feedback, get_all_staff,
    get_staff_by_id, get_all_salons, get_all_services
)


async def handler_main_menu(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'select_salon':
        salon_list = await get_all_salons()

        await query.message.edit_text(
            text='Выберите салон',
            reply_markup=keyboard.salon_menu(salon_list)
        )
        return states_bot.SELECT_SALON

    elif query.data == 'select_master':
        staff_list = await get_all_staff()

        await query.message.edit_text(
            text='Мастер, дата работы и салон',
            reply_markup=keyboard.master_menu(staff_list)
        )
        return states_bot.SELECT_MASTER

    elif query.data == 'send_feedback':
        staff_list = await get_all_staff()

        await query.message.edit_text(
            text='Выберите мастера, о котором хотите оставить отзыв.',
            reply_markup=keyboard.feedback_staff_menu(staff_list)
        )
        return states_bot.SELECT_MASTER_TO_FEEDBACK


async def handler_salon_menu(update, context):
    query = update.callback_query
    await query.answer()

    if query.data.startswith('salon_'):
        procedures_list = await get_all_services()

        context.user_data['salon_id'] = query.data.split('_')[1]  # сохранение id для удобства
        await query.message.edit_text(
            'Выберите процедуру',
            reply_markup=keyboard.procedure_menu(procedures_list)
        )
        return states_bot.SELECT_PROCEDURE

    elif query.data == 'back_to_main':
        text = (
            'Вас приветствует бот салонов красоты BeautyCity.\n\n'
            'Вы можете выбрать салон или мастера, чтобы записаться, а также оставить отзыв.\n\n'
            'Если у вас возникли трудности или вам нужна консультация:\n'
            'Телефон для связи с нами: +79801234567'
        )
        await query.message.edit_text(
            text=text,
            reply_markup=keyboard.main_menu()
        )
        return states_bot.MAIN_MENU


async def handler_procedure_menu(update, context):
    query = update.callback_query
    await query.answer()

    if query.data.startswith('procedure_'):
        context.user_data['procedure_id'] = query.data.split('_')[1]
        await query.message.edit_text(
            'Выберите удобную вам дату',
            reply_markup=keyboard.date_menu()
        )
        return states_bot.SELECT_DATE

    elif query.data == 'back_to_salon':

        if context.user_data.get('master_id'):
            master_list = await get_all_staff()

            context.user_data.pop('master_id', None)
            await query.message.edit_text(
                'Мастер, дата работы и салон',
                reply_markup=keyboard.master_menu(master_list)
            )
            return states_bot.SELECT_MASTER

        else:
            salons_list = await get_all_salons()
            
            await query.message.edit_text(
                'Выберите салон',
                reply_markup=keyboard.salon_menu(salons_list)
            )
            return states_bot.SELECT_SALON


async def handler_date_menu(update, context):
    query = update.callback_query
    await query.answer()

    if query.data.startswith('date_'):
        context.user_data['date'] = query.data.split('_')[1]  # 'yyyy-mm-dd'
        await query.message.edit_text(
            'Выберите время',
            reply_markup=keyboard.time_menu()
        )
        return states_bot.SELECT_TIME

    elif query.data == 'back_to_procedure':
        procedures_list = await get_all_services()

        await query.message.edit_text(
            'Выберите процедуру',
            reply_markup=keyboard.procedure_menu(procedures_list)
        )
        return states_bot.SELECT_PROCEDURE


async def handler_time_menu(update, context):
    query = update.callback_query
    await query.answer()

    if query.data.startswith('time_'):
        context.user_data['time'] = query.data.split('_')[1]  # 'hh:mm'
        await query.delete_message()
        text = (
            'Нам нужно ваше согласие на обработку данных,'
            ' т.к. нам потребуется ваше ФИО и номер телефона.'
        )
        with open('opd/opd.pdf', 'rb') as pdf_file:
            await query.message.reply_document(
                document=pdf_file,
                caption=text,
                reply_markup=keyboard.opd_menu()
            )
        return states_bot.OPD

    elif query.data == 'back_to_date':
        await query.message.edit_text(
            'Выберите удобную вам дату',
            reply_markup=keyboard.date_menu()
        )
        return states_bot.SELECT_DATE


async def handler_opd_menu(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'agree':
        # сюда добавить сохр, что пользователь уже соглашался
        # (для того кто уже был зареган)
        await query.delete_message()
        await query.message.reply_text(
            'Введите фио',
        )
        return states_bot.CLIENT_NAME

    elif query.data == 'disagree':
        context.user_data.clear()  # очистка т.к. возврат в главное меню
        await query.delete_message()
        text = (
            'Вас приветствует бот салонов красоты BeautyCity.\n\n'
            'Вы можете выбрать салон или мастера, чтобы записаться, а также оставить отзыв\n\n'
            'Если у вас возникли трудности или вам нужна консультация:\n'
            'Телефон для связи с нами: +79801234567'
        )
        await query.message.reply_text(
            text=text,
            reply_markup=keyboard.main_menu()
        )
        return states_bot.MAIN_MENU


async def handler_name_menu(update, context):
    context.user_data['name'] = update.message.text
    text = (
        'Введите номер телефона, начиная с 8 или 7.\n'
        'Пример: 79801234567'
    )
    await update.message.reply_text(text=text)
    return states_bot.CLIENT_PHONENUMBER


async def handler_phone_menu(update, context):
    phone = ''.join(filter(str.isdigit, update.message.text))  # получение только цифр из строки для проверки номера телефона

    if len(phone) == 11 and phone[0] in ['7', '8']:
        context.user_data['phone'] = update.message.text
        text = (
            f'Салон {context.user_data.get("salon_id", "id салона")}\n'
            f'Процедура {context.user_data.get("procedure_id", "id процедуры")}\n'
            f'Мастер {context.user_data.get("master_id", "id мастера")}\n'
            f'Дата {context.user_data.get("date", "Дата")}\n'
            f'Время {context.user_data.get("time", "Время")}\n\n'
            'Стоимость xxxx р.\n\n'
            'Подтвердить запись?'
        )
        await update.message.reply_text(
            text=text,
            reply_markup=keyboard.appointment_with_promocode_menu()
        )
        return states_bot.APPOINTMENT

    else:
        text = (
            'Некорректно введён номер, попробуйте еще раз.\n\n'
            'Введите номер телефона, начиная с 8 или 7.\n'
            'Пример: 79801234567'
        )
        await update.message.reply_text(text=text)
        return states_bot.CLIENT_PHONENUMBER


async def handler_appointment_menu(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'confirm_appointment':
        await query.message.edit_text(
            'Запись подтверждена',
            reply_markup=keyboard.back_to_main_menu()
        )
        # тут нужно сохранить в бд
        context.user_data.clear()
        return states_bot.AFTER_APPOINTMENT

    elif query.data == 'cancel_appointment':
        context.user_data.clear()
        await query.message.edit_text(
            'Запись отменена',
            reply_markup=keyboard.back_to_main_menu()
        )
        return states_bot.AFTER_APPOINTMENT

    elif query.data == 'have_promocode':
        await query.message.edit_text(
            'Введите промокод',
            reply_markup=keyboard.back_to_appointment_menu()
        )
        return states_bot.ADD_PROMO


async def handler_add_promo(update, context):
    if update.message and update.message.text:
        context.user_data['promocode'] = update.message.text
        text = (
            f'Салон {context.user_data.get("salon_id", "id салона")}\n'
            f'Процедура {context.user_data.get("procedure_id", "id процедуры")}\n'
            f'Мастер {context.user_data.get("master_id", "id мастера")}\n'
            f'Дата {context.user_data.get("date", "Дата")}\n'
            f'Время {context.user_data.get("time", "Время")}\n'
            f'Промокод {context.user_data.get("promocode", "Промокод")}\n\n'
            'Стоимость xxxx*скидку промокода р.\n\n'
            'Подтвердить запись?'
        )
        await update.message.reply_text(
            text=text,
            reply_markup=keyboard.appointment_menu()
        )
        return states_bot.APPOINTMENT


async def handler_after_appointment(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'back_to_main':
        text = (
            'Вас приветствует бот салонов красоты BeautyCity.\n\n'
            'Вы можете выбрать салон или мастера, чтобы записаться, а также оставить отзыв.\n\n'
            'Если у вас возникли трудности или вам нужна консультация:\n'
            'Телефон для связи с нами: +79801234567'
        )
        await query.message.edit_text(
            text=text,
            reply_markup=keyboard.main_menu()
        )
        return states_bot.MAIN_MENU


async def handler_master_menu(update, context):
    query = update.callback_query
    await query.answer()

    if query.data.startswith('master_'):
        procedures_list = await get_all_services()

        context.user_data['master_id'] = query.data.split('_')[1]
        await query.message.edit_text(
            'Выберите процедуру',
            reply_markup=keyboard.procedure_menu(procedures_list)
        )
        return states_bot.SELECT_PROCEDURE

    elif query.data == 'back_to_main':
        text = (
            'Вас приветствует бот салонов красоты BeautyCity.\n\n'
            'Вы можете выбрать салон или мастера, чтобы записаться, а также оставить отзыв.\n\n'
            'Если у вас возникли трудности или вам нужна консультация:\n'
            'Телефон для связи с нами: +79801234567'
        )
        await query.message.edit_text(
            text=text,
            reply_markup=keyboard.main_menu()
        )
        return states_bot.MAIN_MENU


async def handler_master_feedback_menu(update, context):
    query = update.callback_query
    await query.answer()

    if query.data.startswith('master_'):
        master_id = int(query.data.split('_')[1])

        master = await get_staff_by_id(master_id)  # сервис
        context.user_data['feedback_master_id'] = master.id
        context.user_data['feedback_master_name'] = master.name

        await query.message.edit_text(
            f'Введите отзыв о мастере {master.name}'
        )
        return states_bot.CLIENT_FEEDBACK

    if query.data == 'back_to_main':
        text = (
            'Вас приветствует бот салонов красоты BeautyCity.\n\n'
            'Вы можете выбрать салон или мастера, чтобы записаться, а также оставить отзыв.\n\n'
            'Если у вас возникли трудности или вам нужна консультация:\n'
            'Телефон для связи с нами: +79801234567'
        )
        await query.message.edit_text(
            text=text,
            reply_markup=keyboard.main_menu()
        )
        return states_bot.MAIN_MENU


async def handler_feedback_menu(update, context):
    context.user_data['feedback'] = update.message.text

    await update.message.reply_text(
        'Введите ваше ФИО'
    )
    return states_bot.FEEDBACK_CLIENT_NAME


async def handler_feedback_client_name(update, context):
    context.user_data['feedback_name'] = update.message.text

    await update.message.reply_text(
        'Введите номер телефона (7XXXXXXXXXX или 8XXXXXXXXXX).'
    )
    return states_bot.FEEDBACK_CLIENT_PHONE


async def handler_feedback_client_phone(update, context):
    phone = ''.join(filter(str.isdigit, update.message.text))

    if len(phone) != 11 or phone[0] not in ('7', '8'):
        await update.message.reply_text(
            'Некорректный номер. Попробуйте ещё раз'
        )
        return states_bot.FEEDBACK_CLIENT_PHONE

    context.user_data['feedback_phone'] = phone

    await update.message.reply_text(
        f'''Мастер: {context.user_data['feedback_master_name']}
Отзыв:
{context.user_data['feedback']}''',
        reply_markup=keyboard.confirm_feedback()
    )

    return states_bot.CONFIRM_FEEDBACK_MENU


async def handler_confirm_feedback_menu(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'send':
        client = await get_or_create_client(
            name=context.user_data['feedback_name'],
            phone=context.user_data['feedback_phone']
        )

        await create_feedback(
            staff_id=int(context.user_data['feedback_master_id']),
            client=client,
            text=context.user_data['feedback']
        )

        await query.message.edit_text(
            'Спасибо! Ваш отзыв сохранён.',
            reply_markup=keyboard.back_to_main_menu()
        )

        context.user_data.clear()
        return states_bot.AFTER_FEEDBACK

    elif query.data == 'cancel':
        context.user_data.clear()
        await query.message.edit_text(
            'Отзыв отменён',
            reply_markup=keyboard.back_to_main_menu()
        )
        return states_bot.AFTER_FEEDBACK


async def handler_after_feedback(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'back_to_main':
        text = (
            'Вас приветствует бот салонов красоты BeautyCity.\n\n'
            'Вы можете выбрать салон или мастера, чтобы записаться, а также оставить отзыв.\n\n'
            'Если у вас возникли трудности или вам нужна консультация:\n'
            'Телефон для связи с нами: +79801234567'
        )
        await query.message.edit_text(
            text=text,
            reply_markup=keyboard.main_menu()
        )
        return states_bot.MAIN_MENU
