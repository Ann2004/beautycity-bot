from . import states_bot
from ptb.keyboards import keyboard

from salon.services import (
    get_or_create_client, create_feedback, get_all_staff, get_salon_by_id,
    get_staff_by_id, get_all_salons, get_all_services, get_services_by_staff,
    get_staff_busy_days, get_staff_available_slots, is_staff_available,
    find_available_master_for_slot, get_busy_days_for_salon_service,
    get_available_slots_for_salon_service, get_promo_by_code,
    get_service_by_id, create_appointment
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

        salon_id = int(query.data.split('_')[1])
        context.user_data['salon_id'] = salon_id

        salon = await get_salon_by_id(salon_id)
        context.user_data['salon'] = salon

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
        selected_procedure_id = query.data.split('_')[1]
        context.user_data['procedure_id'] = selected_procedure_id

        service = await get_service_by_id(int(selected_procedure_id))
        context.user_data['service'] = service

        selected_master_id = context.user_data.get('master_id')
        selected_salon_id = context.user_data.get('salon_id')

        if selected_master_id:
            # запись через мастера
            master_busy_days = await get_staff_busy_days(int(selected_master_id), days_ahead=7)

            await query.message.edit_text(
                'Выберите удобную дату',
                reply_markup=keyboard.date_menu_with_availability(master_busy_days)
            )
            return states_bot.SELECT_DATE
        elif selected_salon_id:
            # запись через салон
            salon_busy_days = await get_busy_days_for_salon_service(
                int(selected_salon_id),
                int(selected_procedure_id),
                days_ahead=7
            )

            await query.message.edit_text(
                'Выберите удобную дату',
                reply_markup=keyboard.date_menu_with_availability(salon_busy_days)
            )
            return states_bot.SELECT_DATE

    elif query.data == 'back_to_salon':
        if context.user_data.get('master_id'):
            all_masters = await get_all_staff()

            await query.message.edit_text(
                'Выберите мастера',
                reply_markup=keyboard.master_menu(all_masters)
            )
            return states_bot.SELECT_MASTER

        else:
            all_salons = await get_all_salons()

            await query.message.edit_text(
                'Выберите салон',
                reply_markup=keyboard.salon_menu(all_salons)
            )
            return states_bot.SELECT_SALON


async def handler_date_menu(update, context):
    query = update.callback_query
    await query.answer()

    if query.data.startswith('date_'):
        selected_date_str = query.data.split('_')[1]  # 'yyyy-mm-dd'
        context.user_data['date'] = selected_date_str

        selected_master_id = context.user_data.get('master_id')
        selected_salon_id = context.user_data.get('salon_id')
        selected_procedure_id = context.user_data.get('procedure_id')

        if selected_master_id:
            # запись через мастера
            master_available_slots = await get_staff_available_slots(int(selected_master_id), selected_date_str)

            if not master_available_slots:
                await query.answer(
                    'На эту дату у мастера нет свободного времени. Выберите другую дату.',
                    show_alert=True
                )
                return states_bot.SELECT_DATE

            await query.message.edit_text(
                'Выберите время',
                reply_markup=keyboard.time_menu_with_availability(master_available_slots, selected_date_str)
            )
            return states_bot.SELECT_TIME
        elif selected_salon_id and selected_procedure_id:
            # запись через салон
            salon_available_slots = await get_available_slots_for_salon_service(
                int(selected_salon_id),
                int(selected_procedure_id),
                selected_date_str
            )

            if not salon_available_slots:
                await query.answer(
                    'На эту дату нет свободного времени для выбранной услуги. Выберите другую дату.',
                    show_alert=True
                )
                return states_bot.SELECT_DATE

            await query.message.edit_text(
                'Выберите время',
                reply_markup=keyboard.time_menu_with_availability(salon_available_slots, selected_date_str)
            )
            return states_bot.SELECT_TIME

    elif query.data == 'back_to_procedure':
        all_services = await get_all_services()

        # запись через мастера и его услуги
        selected_master_id = context.user_data.get('master_id')
        if selected_master_id:
            master_services = await get_services_by_staff(int(selected_master_id))
            await query.message.edit_text(
                'Выберите процедуру',
                reply_markup=keyboard.procedure_menu(master_services)
            )
        else:
            await query.message.edit_text(
                'Выберите процедуру',
                reply_markup=keyboard.procedure_menu(all_services)
            )
        return states_bot.SELECT_PROCEDURE


async def handler_time_menu(update, context):
    query = update.callback_query
    await query.answer()

    if query.data.startswith('time_'):
        selected_time = query.data.split('_')[1]  # 'hh:mm'
        selected_date = context.user_data.get('date')

        # запись через мастера
        master_id = context.user_data.get('master_id')
        if master_id and selected_date:
            is_available = await is_staff_available(
                int(master_id),
                selected_date,
                selected_time
            )

            if not is_available:
                await query.answer(
                    'Это время уже занято. Пожалуйста, выберите другое время.',
                    show_alert=True
                )
                return states_bot.SELECT_TIME

            context.user_data['time'] = selected_time

        # запись через салон
        elif selected_date:
            salon_id = context.user_data.get('salon_id')
            service_id = context.user_data.get('procedure_id')

            if salon_id and service_id:
                # свободный мастер
                available_master = await find_available_master_for_slot(
                    int(salon_id),
                    int(service_id),
                    selected_date,
                    selected_time
                )

                if not available_master:
                    await query.answer(
                        'Это время уже занято у всех мастеров. Выберите другое время.',
                        show_alert=True
                    )
                    return states_bot.SELECT_TIME

                context.user_data['master_id'] = str(available_master.id)
                context.user_data['master_name'] = available_master.name
                context.user_data['master'] = available_master
                context.user_data['time'] = selected_time

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
        master_id = context.user_data.get('master_id')

        if master_id:
            # меню даты с учетом занятости
            busy_days_info = await get_staff_busy_days(int(master_id), days_ahead=7)

            await query.message.edit_text(
                'Выберите удобную дату',
                reply_markup=keyboard.date_menu_with_availability(busy_days_info)
            )
        else:
            # меню даты
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
        service = context.user_data['service']
        master = context.user_data['master']
        salon = context.user_data.get('salon')

        if not salon and master:
            salon = master.salon

        text = (
            f'Салон: {salon.address}\n'
            f'Процедура: {service.name}\n'
            f'Мастер: {master.name}\n'
            f'Дата: {context.user_data.get("date", "Дата")}\n'
            f'Время: {context.user_data.get("time", "Время")}\n\n'
            f'Стоимость: {service.price} ₽\n\n'
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
        client = await get_or_create_client(
            name=context.user_data['name'],
            phone=context.user_data['phone'],
            telegram_id=update.effective_user.id
        )

        service = context.user_data['service']
        staff = context.user_data['master']
        promo = context.user_data.get('promo')

        await create_appointment(
            client=client,
            service=service,
            staff=staff,
            appointment_date=context.user_data['date'],
            time=context.user_data['time'],
            promo=promo
        )
        await query.message.edit_text(
            '✅ Запись подтверждена!',
            reply_markup=keyboard.back_to_main_menu()
        )
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
            'Введите промокод'
        )
        return states_bot.ADD_PROMO


async def handler_add_promo(update, context):
    promo_code = update.message.text
    promo = await get_promo_by_code(promo_code)

    service = context.user_data['service']
    master = context.user_data['master']
    salon = context.user_data.get('salon') or master.salon

    if not promo:
        text = (
            '❌ Промокод не найден.\n\n'
            f'Салон: {salon.address}\n'
            f'Процедура: {service.name}\n'
            f'Мастер: {master.name}\n'
            f'Дата: {context.user_data.get("date")}\n'
            f'Время: {context.user_data.get("time")}\n'
            f'Цена: {service.price} ₽\n\n'
            'Подтвердить запись?'
        )

        await update.message.reply_text(
            text=text,
            reply_markup=keyboard.appointment_menu()
        )

        return states_bot.APPOINTMENT

    original_price = service.price
    discount = promo.discount_percent
    final_price = round(original_price * (100 - discount) / 100, 2)

    context.user_data['promo'] = promo
    context.user_data['final_price'] = final_price

    text = (
        f'Салон: {salon.address}\n'
        f'Процедура: {service.name}\n'
        f'Мастер: {master.name}\n'
        f'Дата: {context.user_data.get("date")}\n'
        f'Время: {context.user_data.get("time")}\n\n'
        f'Промокод: {promo.code} (-{promo.discount_percent}%)\n'
        f'Цена без скидки: {original_price} ₽\n'
        f'Цена со скидкой: {final_price} ₽\n\n'
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
        master_id = query.data.split('_')[1]
        context.user_data['master_id'] = master_id

        master = await get_staff_by_id(int(master_id))
        context.user_data['master'] = master

        procedures_list = await get_services_by_staff(int(master_id))  # услуги мастера

        if not procedures_list:
            await query.message.edit_text(
                'У этого мастера пока нет доступных услуг.',
                reply_markup=keyboard.back_to_main_menu()
            )
            return states_bot.MAIN_MENU

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
            phone=context.user_data['feedback_phone'],
            telegram_id=update.effective_user.id
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
