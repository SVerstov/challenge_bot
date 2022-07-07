from telebot import types
from telebot.types import InlineKeyboardButton as ibtn


miss_description_kb = types.InlineKeyboardMarkup()
miss_btn = ibtn('Пропустить описание')
miss_description_kb.add(miss_btn)


measurement_kb = types.InlineKeyboardMarkup()
measurement_kb.row(
    ibtn('В штуках', callback_data='amount'),
    ibtn('В километрах', callback_data='distance'),
)

