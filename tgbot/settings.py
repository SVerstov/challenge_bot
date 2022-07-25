from typing import Dict
import telebot
# from telebot import apihelper, logger
import logging

telebot.apihelper.ENABLE_MIDDLEWARE = True

# LOGGER
logger = telebot.logger
logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.


class ExceptionHandler(telebot.ExceptionHandler):
    def handle(self, exception):
        logger.error(exception)


counter_set = {
    'numbers': {
        '-1': -1,
        '+1': 1,
        '+5': 5,
        '+10': 10,
        '+20': 20,
    },
    'minutes': {
        '-1м': -60,
        '1c': 1,
        '10c': 10,
        '30c': 30,
        '1м': 60,
        '5м': 300,
        '10м': 600,
    },
    'distance': {
        '-1': -1,
        '+0.1': 0.1,
        '+0.5': 0.5,
        '+1': 1,
        '+5': 5,
        '+10': 10,
    },
}

list_of_commands: Dict[str, Dict[str, str]] = {
    'ru': {
        'counter': 'Учёт выполненных упражнений 🧮',
        'stats': 'Статистика 📊',
        'accept': 'Запустить челлендж! 🚀',
        'new_exercise': 'Создать новое упражнение 🏃',
        'new_challenge': 'Создать новый челлендж!🏋🏼‍♂',
        'cansel': 'Отменить текущее действие ⛔',
        'set_timezone': 'Настроить часовой пояс 🕔',
        'delete_exercise': 'Удалить упражнение ❌',
        'delete_challenge': 'Удалить челлендж 🚫',
    },
}
list_of_commands['en'] = list_of_commands['ru']  # todo мультиязычное меню

start_message = "Добро пожаловать! 👋\n" \
                "Этот бот поможет вам пройти один из <b>спортивных челленждей!</b>\n\n" \
                "Для успешного прохождения необходимо выполнить определенный объём упражнений за отведенное время.\n" \
                "Например: <i>5000 отжиманий за месяц.</i>\n\n" \
                "При этом как и когда выполнять упражнения не уточняется. Их можно выполнять раз в сутки," \
                " а можно 'размазывать' на весь день. Экспериментируйте. 💪\n\n" \
                "Принять челлендж /accept\n" \
                "Учёт упражнений /counter\n" \
                "Настроить часовой пояс /set_timezone\n" \
                "А для всего остального есть меню =)"
