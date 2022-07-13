from telebot import types

from tgbot.create_bot import bot


@bot.message_handler()
def unidentified_command(message: types.Message):
    bot.reply_to(message, "Неопознанная команда")
