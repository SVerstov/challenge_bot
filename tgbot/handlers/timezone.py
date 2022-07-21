from telebot import types
from telebot.handler_backends import StatesGroup, State

from tgbot.create_bot import bot
from tgbot.keyboards.settings_kb import timezone_kb
from tgbot.utils import get_or_save_user


class TimeZoneState(StatesGroup):
    set_timezone = State()


@bot.message_handler(commands=['set_timezone'])
def send_help_info(message: types.Message):
    chat_id = message.chat.id
    user = get_or_save_user(message)
    bot.set_state(chat_id, TimeZoneState.set_timezone)
    tz = user.time_zone
    sign = '+' if tz > 0 else ''
    bot.send_message(chat_id, f"Текущий часовой пояс: {sign}{tz}\n"
                              f"Выберите часовой пояс:", reply_markup=timezone_kb)


@bot.callback_query_handler(func=lambda c: int(c.data) in range(-11, 13), state=TimeZoneState.set_timezone)
def timezone_selected(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    user = get_or_save_user(call.message)
    user.time_zone = int(call.data)
    user.save()

    tz = user.time_zone
    sign = '+' if tz > 0 else ''
    bot.send_message(chat_id, f"Текущий часовой пояс: {sign}{tz}")
    bot.answer_callback_query(call.id)
    bot.delete_state(chat_id)
