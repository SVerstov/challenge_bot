from telebot.types import KeyboardButton as Btn, ReplyKeyboardMarkup


def get_markup_kb(*args, one_time_kb = False, row_width=3):
    one_time_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time_kb, row_width=row_width)
    keys = (Btn(key) for key in args)
    one_time_kb.add(*keys)
    return one_time_kb

