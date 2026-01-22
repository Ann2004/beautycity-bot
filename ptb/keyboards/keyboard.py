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
    keyboard = [
        [InlineKeyboardButton('dd.mm.yyyy', callback_data='date_yyyy-mm-dd')],
        [InlineKeyboardButton('Назад', callback_data='back_to_procedure')]
    ]

    return InlineKeyboardMarkup(keyboard)


def time_menu():
    keyboard = [
        [InlineKeyboardButton('hh:mm', callback_data='time_hh:mm')],
        [InlineKeyboardButton('Назад', callback_data='back_to_date')]
    ]

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


def opd_menu():
    keyboard = [
        [InlineKeyboardButton('Согласиться', callback_data='agree')],
        [InlineKeyboardButton('Отказаться', callback_data='disagree')]
    ]
    return InlineKeyboardMarkup(keyboard)