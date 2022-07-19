import datetime
import random

from telebot import types

from server.models import User, AcceptedExerciseSet


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


def get_exercise_progress_info(exercise: AcceptedExerciseSet, today: bool = False, percent: bool = False) -> str:
    info = f'*{exercise.name}:*\n' \
           f' {exercise.progress:g} {exercise.get_measurement_display().lower()} из {exercise.amount}'
    if today:
        info += f' | Сегодня: {exercise.progress_on_last_day: g}'
    if percent:
        info += f' | Проценты' #todo проценнты
    return info


def get_today_date(timezone: int):
    """ :returns current date considering UTC timezone"""
    offset = datetime.timedelta(hours=timezone)
    tz = datetime.timezone(offset, name='тест')
    return datetime.datetime.now(tz=tz).date()