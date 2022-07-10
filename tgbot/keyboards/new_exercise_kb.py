from telebot import types
from telebot.types import InlineKeyboardButton as Ibtn


miss_description_kb = types.InlineKeyboardMarkup()
miss_btn = Ibtn('Пропустить описание', callback_data='miss_description')
miss_description_kb.add(miss_btn)


measurement_kb = types.InlineKeyboardMarkup()
measurement_kb.row(
    Ibtn('В штуках', callback_data='amount'),
    Ibtn('В километрах', callback_data='distance'),
    Ibtn('В минутах', callback_data='minutes'),
)

