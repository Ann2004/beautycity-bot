from datetime import datetime, timedelta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu():
    keyboard = [
        [InlineKeyboardButton('Выбрать салон', callback_data='select_salon')],
        [InlineKeyboardButton('Запись к мастеру', callback_data='select_master')],
        [InlineKeyboardButton('Оставить отзыв', callback_data='send_feedback')],
    ]

    return InlineKeyboardMarkup(keyboard)


def salon_menu():
    keyboard = [
        [InlineKeyboardButton('Название салона и адрес', callback_data='salon_1')],
        [InlineKeyboardButton('Назад', callback_data='back_to_main')]
    ]

    return InlineKeyboardMarkup(keyboard)


def master_menu():
    keyboard = [
        [InlineKeyboardButton('Мастер', callback_data='master_1')],
        [InlineKeyboardButton('Назад', callback_data='back_to_main')]
    ]

    return InlineKeyboardMarkup(keyboard)


def feedback_menu():
    keyboard = [
        [InlineKeyboardButton('Мастер', callback_data='master_1')],
        [InlineKeyboardButton('Назад', callback_data='back_to_main')]
    ]

    return InlineKeyboardMarkup(keyboard)


def confirm_feedback():
    keyboard = [
        [InlineKeyboardButton('Отравить', callback_data='send')],
        [InlineKeyboardButton('Отменить', callback_data='cancel')]
    ]

    return InlineKeyboardMarkup(keyboard)


def procedure_menu():
    keyboard = [
        [InlineKeyboardButton('Название процедуры и стоимость', callback_data='procedure_1')],
        [InlineKeyboardButton('Назад', callback_data='back_to_salon')]
    ]

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


def time_menu():
    times = [f"{hour:02d}:00" for hour in range(10, 20)]
    keyboard = [
        [
            InlineKeyboardButton(times[i], callback_data=f'time_{times[i]}'),
            InlineKeyboardButton(times[i+1], callback_data=f'time_{times[i+1]}')
        ]
        for i in range(0, len(times), 2)
    ]

    keyboard.append([InlineKeyboardButton('Назад', callback_data='back_to_date')])

    return InlineKeyboardMarkup(keyboard)


def opd_menu():
    keyboard = [
        [InlineKeyboardButton('Согласиться', callback_data='agree')],
        [InlineKeyboardButton('Отказаться', callback_data='disagree')]
    ]

    return InlineKeyboardMarkup(keyboard)


def promocode_menu():
    keyboard = [
        [InlineKeyboardButton('Пропустить', callback_data='skip_promo')]
    ]

    return InlineKeyboardMarkup(keyboard)


def appointment_menu():
    keyboard = [
        [InlineKeyboardButton('Подтвердрить запись', callback_data='confirm_appointment')],
        [InlineKeyboardButton('Отменить запись', callback_data='cancel_appointment')]
    ]

    return InlineKeyboardMarkup(keyboard)


def appointment_with_promocode_menu():
    keyboard = [
        [InlineKeyboardButton('Подтвердрить запись', callback_data='confirm_appointment')],
        [InlineKeyboardButton('У меня есть промокод', callback_data='have_promocode')],
        [InlineKeyboardButton('Отменить запись', callback_data='cancel_appointment')]
    ]

    return InlineKeyboardMarkup(keyboard)


def back_to_appointment_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('Назад', callback_data='back_to_appointment')]
    ])


def back_to_main_menu():
    keyboard = [
        [InlineKeyboardButton('Вернуться в главное меню', callback_data='back_to_main')]
    ]

    return InlineKeyboardMarkup(keyboard)
