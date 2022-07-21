from telebot.types import InlineKeyboardButton as Ibtn, InlineKeyboardMarkup

timezone_kb = InlineKeyboardMarkup(row_width=8)

keys = []
for i in range(-11,13):
    tz = f'+{i}' if i>0 else str(i)
    keys.append(Ibtn(tz, callback_data=str(i)))
timezone_kb.row(*keys)