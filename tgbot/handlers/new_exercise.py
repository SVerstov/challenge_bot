from telebot import custom_filters
from telebot import types
from telebot.handler_backends import State, StatesGroup

from server.models import Exercise
from tgbot.keyboards.new_exercise_kb import miss_description_kb, measurement_kb
from tgbot.utils import Bot


class AddExerciseState(StatesGroup):
    name = State()
    description = State()
    measurement = State()


@Bot.message_handler(commands='cansel', state='*')
def new_exercise(message: types.Message):
    Bot.send_message(message.chat.id, "Отменяем")
    Bot.delete_state(message.from_user.id)


@Bot.message_handler(commands='new', state='*')
def new_exercise_name(message: types.Message):
    Bot.send_message(message.chat.id, "Создаём новое упражнение!\n Введите его название:")
    Bot.set_state(message.from_user.id, AddExerciseState.name)
    Bot.add_data(message.from_user.id, creator_id=message.from_user.id)


@Bot.message_handler(state=AddExerciseState.name)
def new_exercise_description(message: types.Message):
    Bot.send_message(message.chat.id, "Введите описание", reply_markup=miss_description_kb)
    Bot.set_state(message.from_user.id, AddExerciseState.description)
    Bot.add_data(message.from_user.id, name=message.text)


@Bot.callback_query_handler(func=lambda c: c.data == 'miss_description', state=AddExerciseState.description)
def miss_callback(call: types.CallbackQuery):
    Bot.answer_callback_query(call.id)
    Bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id, reply_markup='')
    Bot.set_state(call.message.chat.id, AddExerciseState.measurement)
    Bot.send_message(call.message.chat.id, "Пропустили. Как будем измерять?", reply_markup=measurement_kb)


@Bot.message_handler(state=AddExerciseState.description)
def new_exercise_measurement(message: types.Message):
    Bot.send_message(message.chat.id, "Как будем измерять ваше упражнение?", reply_markup=measurement_kb)
    Bot.set_state(message.from_user.id, AddExerciseState.measurement)
    Bot.add_data(message.from_user.id, description=message.text)


""" +++++++++++++++++++++++++++++++++++++++++++ """


@Bot.callback_query_handler(func=lambda call: True, state=AddExerciseState.measurement)
def miss_callback(call: types.CallbackQuery):
    Bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id, reply_markup='')
    with Bot.retrieve_data(call.message.chat.id) as data:
        data['measurement'] = call.data

        if save_new_exercise(data):
            Bot.send_message(call.message.chat.id, f'Упражнение "{data["name"]}" создано!')
        else:
            Bot.send_message(call.message.chat.id, f'Что-то пошло не так')
    Bot.delete_state(call.message.chat.id)
    Bot.answer_callback_query(call.id)


@Bot.message_handler(state=AddExerciseState.measurement)
def new_exercise_save(message: types.Message):
    Bot.send_message(message.chat.id, 'Как будем измерять ваше упражнение?', reply_markup=measurement_kb)


def save_new_exercise(data: dict):
    """ data: telegram_id, name, description, measurement """
    return Exercise.objects.create(**data)


Bot.add_custom_filter(custom_filters.StateFilter(Bot))
# Bot.add_custom_filter(custom_filters.IsDigitFilter())
