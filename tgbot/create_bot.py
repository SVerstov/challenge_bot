import os
from typing import Dict

import telebot.types
from telebot import StateMemoryStorage, TeleBot, custom_filters

API_TOKEN = os.getenv('TG_API_TOKEN')
state_storage = StateMemoryStorage()
bot = TeleBot(API_TOKEN, state_storage=state_storage, parse_mode='Markdown')


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())


list_of_commands: Dict[str, Dict[str, str]] = {
    'ru': {
        'start_challenge': 'Запустить челлендж! 🚀',
        'stats': 'Статистика 📊',
        'new_exercise': 'Создать новое упражнение 🏃',
        'new_challenge': 'Создать новый челлендж!🏋🏼‍♂',
        'cansel': 'Отменить текущее действие',
    },
    'en': {
        'start': 'Start django bot 🚀',
        'stats': 'Statistics of bot 📊',
        # todo заполнить
    },
    'es': {
        'start': 'Iniciar el bot de django 🚀',
        'stats': 'Estadísticas de bot 📊',
    },
    'fr': {
        'start': 'Démarrer le bot Django 🚀',
        'stats': 'Statistiques du bot 📊',
    },
}


def set_up_commands(telegram_id: int, language_code: str) -> None:
    if language_code in ['ukr', 'bel']:
        language_code = 'ru'
    elif language_code not in list_of_commands:
        language_code = 'en'
    commands = list_of_commands[language_code]
    bot.set_my_commands(
        commands=[telebot.types.BotCommand(cmd, description) for cmd, description in commands.items()],
        scope=telebot.types.BotCommandScopeChat(telegram_id)
    )
