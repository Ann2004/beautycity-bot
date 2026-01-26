from datetime import datetime, timedelta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu():
    keyboard = [
        [InlineKeyboardButton('Выбрать салон', callback_data='select_salon')],
        [InlineKeyboardButton('Запись к мастеру', callback_data='select_master')],
        [InlineKeyboardButton('Оставить отзыв', callback_data='send_feedback')],
    ]

    return InlineKeyboardMarkup(keyboard)


def salon_menu(salon_list):
    keyboard = []

    for salon in salon_list:
        keyboard.append([
            InlineKeyboardButton(
                text=salon.address,
                callback_data=f'salon_{salon.id}'
            )
        ])

    keyboard.append([
        InlineKeyboardButton('Назад', callback_data='back_to_main')
    ])

    return InlineKeyboardMarkup(keyboard)


def master_menu(master_list):
    keyboard = []

    for master in master_list:
        keyboard.append([
            InlineKeyboardButton(
                text=f'{master.name} ({master.salon.address})',
                callback_data=f'master_{master.id}'
            )
        ])

    keyboard.append([
        InlineKeyboardButton('Назад', callback_data='back_to_main')
    ])

    return InlineKeyboardMarkup(keyboard)


def feedback_staff_menu(staff_list):
    keyboard = []

    for staff in staff_list:
        keyboard.append([
            InlineKeyboardButton(
                text=staff.name,
                callback_data=f'master_{staff.id}'
            )
        ])

    keyboard.append([
        InlineKeyboardButton('Назад', callback_data='back_to_main')
    ])

    return InlineKeyboardMarkup(keyboard)


def confirm_feedback():
    keyboard = [
        [InlineKeyboardButton('Отправить', callback_data='send')],
        [InlineKeyboardButton('Отменить', callback_data='cancel')]
    ]

    return InlineKeyboardMarkup(keyboard)


def procedure_menu(procedures_list):
    keyboard = []

    for procedure in procedures_list:
        keyboard.append([
            InlineKeyboardButton(
                text=f'{procedure.name} ({procedure.price} р.)',
                callback_data=f'procedure_{procedure.id}'
            )
        ])

    keyboard.append([
        InlineKeyboardButton('Назад', callback_data='back_to_salon')
    ])
    return InlineKeyboardMarkup(keyboard)


def date_menu():
    today = datetime.now().date()
    keyboard = []
    days_added = 0
    current_date = today

    while days_added < 7:  # набор 7 дней
        weekday = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вск'][current_date.weekday()]
        date_str = current_date.strftime('%d.%m')

        if current_date == today:
            text = 'Сегодня'
        elif current_date == today + timedelta(days=1):
            text = 'Завтра'
        else:
            text = f'{date_str} {weekday}'

        callback_data = f'date_{current_date.strftime("%Y-%m-%d")}'
        keyboard.append([InlineKeyboardButton(text, callback_data=callback_data)])

        days_added += 1
        current_date += timedelta(days=1)

    keyboard.append([InlineKeyboardButton('Назад', callback_data='back_to_procedure')])

    return InlineKeyboardMarkup(keyboard)


def opd_menu():
    keyboard = [
        [InlineKeyboardButton('Согласиться', callback_data='agree')],
        [InlineKeyboardButton('Отказаться', callback_data='disagree')]
    ]

    return InlineKeyboardMarkup(keyboard)


def appointment_menu():
    keyboard = [
        [InlineKeyboardButton('Подтвердить запись', callback_data='confirm_appointment')],
        [InlineKeyboardButton('Отменить запись', callback_data='cancel_appointment')]
    ]

    return InlineKeyboardMarkup(keyboard)


def appointment_with_promocode_menu():
    keyboard = [
        [InlineKeyboardButton('Подтвердить запись', callback_data='confirm_appointment')],
        [InlineKeyboardButton('У меня есть промокод', callback_data='have_promocode')],
        [InlineKeyboardButton('Отменить запись', callback_data='cancel_appointment')]
    ]

    return InlineKeyboardMarkup(keyboard)


def back_to_main_menu():
    keyboard = [
        [InlineKeyboardButton('Вернуться в главное меню', callback_data='back_to_main')]
    ]

    return InlineKeyboardMarkup(keyboard)


def to_main_menu():
    keyboard = [
        [InlineKeyboardButton('📅 Записаться', url=f't.me/beautycityy_bot?start=menu')]
    ]

    return InlineKeyboardMarkup(keyboard)


def date_menu_with_availability(busy_days_info, days_ahead=7):   # {'2024-01-01': ['10:00', '14:00'], ...}
    today = datetime.now().date()
    current_time = datetime.now().time()
    keyboard = []
    days_added = 0
    current_date = today

    while days_added < days_ahead:
        date_str = current_date.isoformat()
        weekday = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вск'][current_date.weekday()]
        date_display = current_date.strftime('%d.%m')

        # для текущего дня
        is_today = current_date == today
        skip_day = False

        if is_today and date_str in busy_days_info:
            # фильтрация прошедших интервалов
            available_times = []
            for time_slot in busy_days_info[date_str]:
                time_parts = time_slot.split(':')
                if len(time_parts) == 2:
                    hour = int(time_parts[0])
                    minute = int(time_parts[1])
                    slot_time = datetime.combine(current_date, datetime.min.time()).replace(hour=hour, minute=minute).time()
                    if slot_time > current_time:
                        available_times.append(time_slot)

            # пропуск дня, если вышло за 19:00
            if not available_times:
                skip_day = True

        if not skip_day:
            if current_date == today:
                text = 'Сегодня'
            elif current_date == today + timedelta(days=1):
                text = 'Завтра'
            else:
                text = f'{date_display} {weekday}'

            # день полностью забит
            if date_str in busy_days_info and len(busy_days_info[date_str]) == 0 and not is_today:
                text = f'{text} ❌'
                callback_data = 'unavailable'
            else:
                callback_data = f'date_{date_str}'

            keyboard.append([InlineKeyboardButton(text, callback_data=callback_data)])

        days_added += 1
        current_date += timedelta(days=1)

    keyboard.append([InlineKeyboardButton('Назад', callback_data='back_to_procedure')])

    return InlineKeyboardMarkup(keyboard)


def time_menu_with_availability(available_slots, selected_date_str=None):
    keyboard = []

    filtered_slots = available_slots
    if selected_date_str:
        today = datetime.now().date()
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()

        if selected_date == today:
            now = datetime.now()
            current_time = now.time()

            filtered_slots = []
            for slot in available_slots:
                # парсинг 'hh:mm'
                slot_parts = slot.split(':')
                if len(slot_parts) == 2:
                    slot_hour = int(slot_parts[0])
                    slot_minute = int(slot_parts[1])
                    slot_time = datetime.combine(today, datetime.min.time()).replace(hour=slot_hour, minute=slot_minute).time()

                    if slot_time > current_time:
                        filtered_slots.append(slot)

    for i in range(0, len(filtered_slots), 2):
        row = []
        row.append(InlineKeyboardButton(
            filtered_slots[i],
            callback_data=f'time_{filtered_slots[i]}'
        ))

        if i + 1 < len(filtered_slots):
            row.append(InlineKeyboardButton(
                filtered_slots[i + 1],
                callback_data=f'time_{filtered_slots[i + 1]}'
            ))

        keyboard.append(row)

    keyboard.append([InlineKeyboardButton('Назад', callback_data='back_to_date')])

    return InlineKeyboardMarkup(keyboard)


def back_to_procedure_menu():
    keyboard = [
        [InlineKeyboardButton('Назад к выбору процедуры', callback_data='back_to_procedure')]
    ]
    return InlineKeyboardMarkup(keyboard)
