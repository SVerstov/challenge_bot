from telebot import types
from telebot.types import InlineKeyboardButton as Ibtn

from tgbot.create_bot import bot

exercises = ['Подтягивание', 'Отжимания', 'Бег', 'Планка']

test_kb = types.InlineKeyboardMarkup()
test_kb.max_row_keys = 6
test_kb.row(
    Ibtn('-1', callback_data='test -1'),
    Ibtn('+0.1', callback_data='test 0.1'),
    Ibtn('+1', callback_data='test 1'),
    Ibtn('+5', callback_data='test 5'),
    Ibtn('+10', callback_data='test 10'),
    Ibtn('+100', callback_data='test 100'),

)


@bot.message_handler(commands=['test'])
def test(message: types.Message):
    for exercise in exercises:
        bot.send_message(message.chat.id, f'*{exercise}*', reply_markup=test_kb)


@bot.callback_query_handler(func=lambda c: c.data.startswith('test'))
def test_call(call: types.CallbackQuery):
    number = float(call.data.split()[1])
    bot.edit_message_text(f'{number:g}', chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=test_kb)
    bot.answer_callback_query(call.id, f'{number:g}')