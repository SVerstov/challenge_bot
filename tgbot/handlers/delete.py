from telebot.handler_backends import StatesGroup, State

import challenge_bot.settings
from tgbot.create_bot import bot
from telebot import types

from tgbot.keyboards.exercises_kb import get_exercises_kb
from tgbot.utils import get_or_save_user, show_all_challenges


class DeleteState(StatesGroup):
    delete_challenge = State()
    delete_exercise = State()


@bot.message_handler(commands=['delete_challenge'])
def delete_challenge(message: types.Message):
    chat_id = message.from_user.id
    bot.set_state(chat_id, DeleteState.delete_challenge)
    show_all_challenges(chat_id, action='delete')


@bot.callback_query_handler(func=lambda c: c.data.isdigit(), state=DeleteState.delete_challenge)
def delete_challenge_callback(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    user = get_or_save_user(call.message)
    challenge_id = int(call.data)

    challenge = user.challenges_set.get(pk=challenge_id)
    challenge_name = challenge.name
    challenge.delete()
    bot.send_message(chat_id, f'{challenge_name}- удалено 🚫')
    bot.delete_state(chat_id)
    bot.answer_callback_query(call.id)


@bot.message_handler(commands=['delete_exercise'])
def delete_exercise(message: types.Message):
    chat_id = message.from_user.id
    kb = get_exercises_kb(chat_id, for_all=False)
    bot.send_message(chat_id, 'Нажмите на упражнение для удаления', reply_markup=kb)
    bot.set_state(chat_id, DeleteState.delete_exercise)


@bot.callback_query_handler(func=lambda c: c.data.isdigit(), state=DeleteState.delete_exercise)
def delete_exercise_call_back(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    user = get_or_save_user(call.message)
    exercise_id = int(call.data)

    exercise = user.exercisesall_set.get(pk=exercise_id)
    exercise_name = exercise.name
    exercise.delete()
    bot.send_message(chat_id, f'{exercise_name}- удалено 🚫')
    bot.delete_state(chat_id)
    bot.answer_callback_query(call.id)