from telebot.custom_filters import TextFilter

from tgbot.settings import start_message
from tgbot.utils import get_or_save_user, set_up_commands, make_info_text
from tgbot.create_bot import bot
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


@bot.message_handler(commands=['start', 'help'])
def start_info(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, start_message, parse_mode='Html')
    set_up_commands(telegram_id=message.from_user.id, language_code=message.from_user.language_code)
    get_or_save_user(message)


@bot.message_handler(text=TextFilter(starts_with='/stats', ignore_case=True), state='*')
def show_info(message: types.Message):
    chat_id = message.chat.id
    user = get_or_save_user(message)
    if user.challenge_accepted:
        info = make_info_text(user)
        bot.send_message(chat_id, info, parse_mode='Markdown')
    else:
        bot.send_message(chat_id, "Нет активных челленджей 😢\n"
                                  "Используйте команду /accept чтобы запустить один из них.")


