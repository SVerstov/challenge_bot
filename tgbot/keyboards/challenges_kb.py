import random

from telebot import types
from telebot.types import InlineKeyboardButton as Ibtn


def get_pick_challenge_kb(name: str, challenge_id: int):
    pick_kb = types.InlineKeyboardMarkup()
    pick_kb.add(Ibtn(f'{name} - Принять вызов!  {get_cool_smile()}', callback_data=challenge_id))
    return pick_kb


reset_kb = types.InlineKeyboardMarkup()
reset_kb.add(Ibtn('Отменить прохождение челленджа 😱', callback_data='reset_challenge'))


def get_delete_challenge_kb(name: str, challenge_id: int):
    delete_kb = types.InlineKeyboardMarkup()
    delete_kb.add(Ibtn(f'{name} - Удалить ❌', callback_data=challenge_id))
    return delete_kb


def get_cool_smile():
    smile_list = '😎 👊🏼 👍🏻 💪 🏋🏼‍♂️ 🤸🏽‍♀️ 🥊 🦾 🤺 ⚔️'
    return random.choice(smile_list.split())


miss_description_kb = types.InlineKeyboardMarkup()
miss_btn = Ibtn('Пропустить', callback_data='miss_description')
miss_description_kb.add(miss_btn)


measurement_kb = types.InlineKeyboardMarkup()
measurement_kb.row(
    Ibtn('В штуках', callback_data='numbers'),
    Ibtn('В километрах', callback_data='distance'),
    Ibtn('В минутах', callback_data='minutes'),
)


offer_to_finish = types.InlineKeyboardMarkup()
offer_to_finish.row(
    Ibtn('Добавить упражнение 💪', callback_data='add_exercise'),
    Ibtn('Сохранить 💾', callback_data='finish'),
)