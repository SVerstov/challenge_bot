from telebot import types

from server.models import User
import random


def get_or_save_user(message: types.Message) -> User:
    telegram_id = message.from_user.id
    user = User.objects.filter(telegram_id=telegram_id).first()
    if not user:
        user = create_user(message)
    return user


def create_user(message):
    telegram_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    language_code = message.from_user.language_code
    user = User.objects.create(telegram_id=telegram_id,
                               username=username,
                               first_name=first_name,
                               last_name=last_name,
                               language_code=language_code)
    return user


def get_cool_smile():
    smile_list = '😎 👊🏼 👍🏻 💪 🏋🏼‍♂️ 🤸🏽‍♀️ 🥊 🦾 🤺 ⚔️'
    return random.choice(smile_list.split())
