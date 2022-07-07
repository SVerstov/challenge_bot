from telebot import types
from telebot.types import KeyboardButton as btn

test_kb = types.ReplyKeyboardMarkup()
test_kb.add(btn('/start'),btn('/help'))