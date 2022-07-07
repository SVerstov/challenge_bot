import telebot
import os

from server.models import User


def get_telebot():
    API_TOKEN = os.getenv('TG_API_TOKEN')
    return telebot.TeleBot(API_TOKEN, parse_mode=None)


def dispatch(data: dict) -> None:
    if 'message' in data:
        user = get_user_from_telegram(data, 'message')
        if text := data['message'].get('text', None):
            if text in ['/start', '/hello']:
                bot = get_telebot()
                bot.send_message(user.user_id, 'hello')
        try:
            pass
        except Exception as e:
            print(e)


def get_user_from_telegram(data, message_type) -> User:
    if message_type == 'message':
        user, created = User.objects.get_or_create(user_id=data['message']['from']['id'], username='', first_name='', last_name='', language_code='')
        return user
