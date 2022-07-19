from telebot import types
from telebot.handler_backends import State, StatesGroup

from server.models import ExercisesAll
from tgbot.keyboards.user_create_kb import measurement_kb
from tgbot.create_bot import bot


class AddExerciseState(StatesGroup):
    description = State()
    measurement = State()


@bot.message_handler(commands=['new_exercise'], state='*')
def new_exercise_name(message: types.Message):
    chat_id = message.chat.id
    bot.reset_data(chat_id)
    bot.send_message(chat_id, "Создаём новое упражнение!\n Введите его название:")
    bot.set_state(chat_id, AddExerciseState.description)
    bot.add_data(chat_id, owner_id=chat_id)
    # TODO проверка, что упражнение уже есть


@bot.message_handler(state=AddExerciseState.description)
def new_exercise_measurement(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Как будем измерять ваше упражнение?", reply_markup=measurement_kb)
    bot.set_state(chat_id, AddExerciseState.measurement)
    bot.add_data(chat_id, name=message.text.strip())


@bot.callback_query_handler(func=lambda call: True, state=AddExerciseState.measurement)
def new_exercise_save(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    with bot.retrieve_data(chat_id) as data:
        data['measurement'] = call.data
        save_new_exercise(data)
        bot.send_message(chat_id, f'Упражнение "{data["name"]}" создано!')
    bot.delete_state(chat_id)
    bot.answer_callback_query(call.id)


def save_new_exercise(data: dict):
    """ use data: owner_id, name, measurement """
    return ExercisesAll.objects.create(**data)


