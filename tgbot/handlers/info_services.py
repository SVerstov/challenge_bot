from typing import Dict

from tgbot.utils import get_or_save_user
from tgbot.create_bot import bot, set_up_commands

from telebot import types


@bot.message_handler(commands=['start'])
def start_info(message: types.Message):
    bot.send_message(message.chat.id, 'Стартанули)!')
    set_up_commands(telegram_id=message.from_user.id, language_code=message.from_user.language_code)
    get_or_save_user(message)


@bot.message_handler(commands=['help'])
def send_help_info(message: types.Message):
    bot.send_message(message.chat.id, "I'll help you... later")
    bot.delete_state(message.from_user.id)


@bot.message_handler(commands=['cansel'], state='*')
def cansel(message: types.Message):
    state = bot.get_state(message.from_user.id)
    if state:
        bot.send_message(message.chat.id, "Отменяем")
        bot.delete_state(message.from_user.id)
    else:
        bot.send_message(message.chat.id, "Нечего отменять")