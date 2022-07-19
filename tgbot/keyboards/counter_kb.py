from telebot import types
from telebot.types import InlineKeyboardButton as Ibtn
from tgbot.keyboards import get_markup_kb

from tgbot.create_bot import bot

def get_counter_kb(exercise_id):
    accounting_kb = types.InlineKeyboardMarkup()
    accounting_kb.max_row_keys = 6
    # todo переписать нормально
    accounting_kb.row(
        Ibtn('-1', callback_data=f'{exercise_id} -1'),
        Ibtn('+0.1', callback_data=f'{exercise_id} 0.1'),
        Ibtn('+1', callback_data=f'{exercise_id} 1'),
        Ibtn('+5', callback_data=f'{exercise_id} 5'),
        Ibtn('+10', callback_data=f'{exercise_id} 10'),
        Ibtn('Своё', callback_data=f'{exercise_id} another')
    )
    return accounting_kb



counter_stats_kb = get_markup_kb('/counter 🧮', '/stats 📊')