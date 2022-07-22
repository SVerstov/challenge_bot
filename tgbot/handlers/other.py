from telebot import types

from tgbot.create_bot import bot


@bot.message_handler()
def unidentified_command(message: types.Message):
    bot.reply_to(message, "Неопознанная команда")


@bot.callback_query_handler(func=lambda c: True, state='*')
def unavailable_call(call: types.CallbackQuery):
    bot.answer_callback_query(call.id,'>>> Кнопка недоступна <<<')