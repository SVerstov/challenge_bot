from tgbot.utils import Bot, get_user

from telebot import types


@Bot.message_handler(commands='start')
def start_info(message: types.Message):
    Bot.send_message(message.chat.id, 'Стартанули!')
    get_user(message)



@Bot.message_handler(commands='help')
def send_help_info(message: types.Message):
    Bot.send_message(message.chat.id, "I'll help you... later")

# @Bot.message_handler(commands='help')
# def send_text(user_id: int, text: str, reply_markup=None):
#     Bot.send_message(user_id, text, reply_markup=reply_markup)
