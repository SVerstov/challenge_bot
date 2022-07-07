from telegram_bot.utils import get_telebot
from telegram_bot.keyboards.test_keyboard import test_kb


def send_help_info(user_id: int):
    bot = get_telebot()
    bot.send_message(user_id, "I'll help you... later",  reply_markup=test_kb)


def send_text(user_id: int, text: str, reply_markup=None):
    bot = get_telebot()
    bot.send_message(user_id, text, reply_markup=reply_markup)
