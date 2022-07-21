from telebot import types
from telebot.apihelper import ApiTelegramException
from telebot.custom_filters import TextFilter
from telebot.handler_backends import State, StatesGroup

from tgbot.keyboards.counter_kb import get_counter_kb, counter_stats_kb
from tgbot.create_bot import bot
from tgbot.utils import get_or_save_user, get_exercise_progress_info
from datetime import date
from server.models import AcceptedExerciseSet
from tgbot.utils import get_today_date, is_challenge_finished
from tgbot.handlers.info_services import show_info


class CounterState(StatesGroup):
    counter_on = State()
    enter_custom_value = State()


@bot.message_handler(text=TextFilter(starts_with=('/учет', '/учёт', '/counter'), ignore_case=True), state='*')
def show_all_exercises_counter(message: types.Message):
    chat_id = message.chat.id
    user = get_or_save_user(message)

    if user.challenge_accepted:
        exercises = user.challenge_accepted.acceptedexerciseset_set.all()
        bot.send_message(chat_id, user.challenge_accepted.name)
        for exercise in exercises:
            kb = get_counter_kb(exercise.id, measerment=exercise.measurement)
            bot.send_message(chat_id, get_exercise_progress_info(exercise, today=True), reply_markup=kb)
        bot.set_state(chat_id, state=CounterState.counter_on)
        bot.add_data(chat_id, exercises=exercises, timezone=user.time_zone)


    else:
        bot.send_message(chat_id, 'Сперва вам нужно принять один из челленджей!\n'
                                  'Используйте команду /accept')


@bot.callback_query_handler(func=lambda c: True, state=[CounterState.counter_on, CounterState.enter_custom_value])
def accounting(call: types.CallbackQuery):  # todo переоткрытие счетчиков,если сообщение висит >48 часов
    chat_id = call.message.chat.id
    exercise_id = int(call.data.split()[0])
    value = call.data.split()[1]
    with bot.retrieve_data(chat_id) as data:
        exercises = data.get('exercises')

        exercise = exercises.get(id=exercise_id)
        exercise: AcceptedExerciseSet

    if value == 'another':
        # Enter custom value
        bot.send_message(chat_id, f'({exercise.name}) Введите число:')
        bot.set_state(chat_id, state=CounterState.enter_custom_value)
        bot.add_data(chat_id, exercise=exercise, message_to_edit_id=call.message.id)
        bot.answer_callback_query(call.id)
    else:
        # get value from button, increase progress
        try:
            delta = float(value)
        except ValueError:
            return

        timezone = data.get('timezone')
        save_exercise_progress(exercise, delta, timezone=timezone)

        kb = get_counter_kb(exercise.id, measerment=exercise.measurement)
        try:
            bot.edit_message_text(get_exercise_progress_info(exercise, today=True),
                                  chat_id=call.message.chat.id,
                                  message_id=call.message.id,
                                  reply_markup=kb)
        except ApiTelegramException:
            # show new counter if edited message is too old
            bot.send_message(chat_id, '🔽🔻🔽🔻🔽🔻Пересоздаю клавиатуру🔻🔽🔻🔽🔻🔽\nПоследнее нажатие было учтено!')
            show_all_exercises_counter(call.message)

        sign = '+' if delta >= 0 else '-'
        bot.answer_callback_query(call.id, f'{exercise.name} {sign}{delta:g}')
        if exercise.progress >= exercise.amount:
            finish_check(call.message)
            bot.edit_message_text()


@bot.message_handler(state=CounterState.enter_custom_value)
def enter_custom_value(message: types.Message):
    """ Get an number from user. increase user progress """
    chat_id = message.chat.id
    try:
        delta = float(message.text)
    except ValueError:
        bot.send_message(chat_id, 'Введите цифры, без букв')
        return

    with bot.retrieve_data(chat_id) as data:
        exercise = data.get('exercise')
        message_to_edit_id = data.get('message_to_edit_id')
        timezone = data.get('timezone')

    save_exercise_progress(exercise, delta, timezone)

    reply_msg = get_exercise_progress_info(exercise, today=True)
    kb = get_counter_kb(exercise.id)
    bot.edit_message_text(reply_msg, chat_id=chat_id, message_id=message_to_edit_id, reply_markup=kb)
    bot.send_message(chat_id, f'Учтено!\n{reply_msg}', reply_markup=counter_stats_kb)
    bot.set_state(chat_id, CounterState.enter_custom_value)
    if exercise.progress >= exercise.amount:
        finish_check(message)


def save_exercise_progress(exercise: AcceptedExerciseSet, delta: float, timezone: int):
    exercise.progress = round(exercise.progress + delta, 2)
    today = get_today_date(timezone)
    if exercise.last_day == today:
        exercise.progress_on_last_day = round(exercise.progress_on_last_day + delta, 2)
    else:
        exercise.progress_on_last_day = delta
        exercise.last_day = today
    exercise.save()


def finish_check(message: types.Message):
    user = get_or_save_user(message)
    if is_challenge_finished(user):
        chat_id = message.chat.id
        show_info(message)
        bot.send_message(chat_id, f'😎 Вы террррминаторрр! Челенж пройден 🏋🏼‍♂️')
        user.challenge_accepted.delete()
        bot.delete_state(chat_id)
