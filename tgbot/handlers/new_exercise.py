from telebot import custom_filters
from telebot import types
from telebot.handler_backends import State, StatesGroup

from server.models import Exercise
from tgbot.keyboards.user_create import miss_description_kb, measurement_kb
from tgbot.create_bot import bot


class AddExerciseState(StatesGroup):
    description = State()
    measurement = State()


@bot.message_handler(commands=['new_exercise'], state='*')
def new_exercise_name(message: types.Message):
    bot.send_message(message.chat.id, "Создаём новое упражнение!\n Введите его название:")
    bot.set_state(message.from_user.id, AddExerciseState.description)
    bot.add_data(message.from_user.id, creator_id=message.from_user.id)
    # todo проверка, что упражнение уже есть


@bot.message_handler(state=AddExerciseState.description)
def new_exercise_measurement(message: types.Message):
    bot.send_message(message.chat.id, "Как будем измерять ваше упражнение?", reply_markup=measurement_kb)
    bot.set_state(message.chat.id, AddExerciseState.measurement)
    bot.add_data(message.chat.id, name=message.text)


@bot.callback_query_handler(func=lambda call: True, state=AddExerciseState.measurement)
def new_exercise_save(call: types.CallbackQuery):
    with bot.retrieve_data(call.message.chat.id) as data:
        data['measurement'] = call.data
        exercise = save_new_exercise(data)
        if exercise:
            bot.send_message(call.message.chat.id, f'Упражнение "{data["name"]}" создано!')
        else:
            bot.send_message(call.message.chat.id, f'Что-то пошло не так')
    bot.delete_state(call.message.chat.id)
    bot.answer_callback_query(call.id)


def save_new_exercise(data: dict):
    """ data: telegram_id, name, description, measurement """
    return Exercise.objects.create(**data)


