from telebot import types
from telebot.types import InlineKeyboardButton as Ibtn
from tgbot.utils import get_cool_smile


def get_pick_challenge_kb(name: str, challenge_id: int):
    pick_kb = types.InlineKeyboardMarkup()
    pick_kb.add(Ibtn(f'{name} - Принять вызов!  {get_cool_smile()}', callback_data=challenge_id))
    return pick_kb
