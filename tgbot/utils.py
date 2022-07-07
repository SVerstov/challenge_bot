import os

import telebot

from server.models import Users
from telebot.storage import StateMemoryStorage

API_TOKEN = os.getenv('TG_API_TOKEN')
state_storage = StateMemoryStorage()
Bot = telebot.TeleBot(API_TOKEN, state_storage=state_storage, parse_mode=None)


def get_telebot():
    return Bot


def get_user_from_telegram(data) -> Users:
    telegram_id = data['message']['from']['id']
    user = Users.objects.filter(telegram_id=telegram_id).first()
    if user is None:
        username = data['message']['from']['username']
        first_name = data['message']['from'].get('first_name')
        last_name = data['message']['from'].get('last_name')
        language_code = data['message']['from'].get('language_code')
        user = Users.objects.create(telegram_id=telegram_id,
                                    username=username,
                                    first_name=first_name,
                                    last_name=last_name,
                                    language_code=language_code)
    return user
