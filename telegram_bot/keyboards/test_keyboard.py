from telebot import types
from telebot.types import KeyboardButton as btn
from telebot.types import InlineKeyboardButton as ibtn

test_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
test_kb.add(btn('/start'),btn('/help'))

inline_kb = types.InlineKeyboardMarkup()
inline_btn1 = ibtn('Вызвать меню', callback_data='/help')
inline_kb.add(inline_btn1)
