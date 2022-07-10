import os

from telebot import TeleBot, types
from telebot.storage import StateMemoryStorage

from server.models import Users

API_TOKEN = os.getenv('TG_API_TOKEN')
state_storage = StateMemoryStorage()
Bot = TeleBot(API_TOKEN, state_storage=state_storage, parse_mode=None)


def get_user(message: types.Message) -> Users:
    telegram_id = message.from_user.id
    user = Users.objects.filter(telegram_id=telegram_id).first()
    if user is None:
        user = create_user(message)
    return user


def create_user(message):
    telegram_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    language_code = message.from_user.language_code
    user = Users.objects.create(telegram_id=telegram_id,
                                username=username,
                                first_name=first_name,
                                last_name=last_name,
                                language_code=language_code)
    return user