from telebot import types
from telebot.types import InlineKeyboardButton as Ibtn
from tgbot.keyboards import get_markup_kb
from tgbot.settings import counter_set

from tgbot.create_bot import bot


def get_counter_kb(exercise_id, measerment: str = 'numbers'):
    accounting_kb = types.InlineKeyboardMarkup()
    accounting_kb.max_row_keys = 8
    keys = [Ibtn(text, callback_data=f'{exercise_id} {callback}') for text, callback in counter_set[measerment].items()]
    keys.append(Ibtn('Своё', callback_data=f'{exercise_id} another'))

    accounting_kb.row(*keys)
    return accounting_kb


counter_stats_kb = get_markup_kb('/counter 🧮', '/stats 📊')
