import logging
import os
from typing import Dict

import telebot.types
from telebot import StateMemoryStorage, TeleBot, custom_filters, logger
from telebot import apihelper

# todo вынести настройки отдельно

apihelper.ENABLE_MIDDLEWARE = True

# LOGGER
logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.


class ExceptionHandler(telebot.ExceptionHandler):
    def handle(self, exception):
        logger.error(exception)


# CREATE BOT
API_TOKEN = os.getenv('TG_API_TOKEN')
state_storage = StateMemoryStorage()
bot = TeleBot(API_TOKEN, state_storage=state_storage, parse_mode='Markdown', exception_handler=ExceptionHandler())

# FILTERS
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())
bot.add_custom_filter(custom_filters.IsDigitFilter())

# COMMANDS
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
list_of_commands['en'] = list_of_commands['ru'] #todo мультиязычное меню


def set_up_commands(telegram_id: int, language_code: str) -> None:
    if language_code in ['ukr', 'bel']:
        language_code = 'ru'
    elif language_code not in list_of_commands:
        language_code = 'en'
    commands = list_of_commands[language_code]
    bot.set_my_commands(
        commands=[telebot.types.BotCommand(cmd, description) for cmd, description in commands.items()],
        scope=telebot.types.BotCommandScopeChat(telegram_id))
