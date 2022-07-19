from telebot.custom_filters import TextFilter

from tgbot.utils import get_or_save_user
from tgbot.create_bot import bot, set_up_commands
from server.models import User
from telebot import types


@bot.message_handler(commands=['cansel'], state='*')
def cansel(message: types.Message):
    chat_id = message.chat.id
    state = bot.get_state(message.from_user.id)
    if state:
        bot.send_message(chat_id, "Отменяем 🚫")
        bot.delete_state(message.from_user.id)
    else:
        bot.send_message(chat_id, "Нечего отменять")


# all commands must reset bot state
@bot.middleware_handler(update_types=['message'])
def middleware_test(bot_instance, message):
    if message.text.startswith('/') and not message.text == '/cansel':
        bot.delete_state(message.from_user.id)


@bot.message_handler(commands=['start'])
def start_info(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Стартанули)!')
    set_up_commands(telegram_id=message.from_user.id, language_code=message.from_user.language_code)
    get_or_save_user(message)


@bot.message_handler(commands=['help'])
def send_help_info(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "I'll help you... later")


@bot.message_handler(text=TextFilter(starts_with='/stats', ignore_case=True), state='*')
def show_info(message: types.Message):
    chat_id = message.chat.id
    user = get_or_save_user(message)
    if user.challenge_accepted:
        info = make_info_text(user)
        bot.send_message(chat_id, info)
    else:
        bot.send_message(chat_id, "Нет активных челленджей 😢\n"
                                  "Используйте команду /accept чтобы запустить один из них.")


def make_info_text(user: User) -> str:
    info = ''
    name = User.challenge_accepted.name

    exercises = user.challenge_accepted.acceptedexerciseset_set
    for exercise in exercises:
        pass
    return info
