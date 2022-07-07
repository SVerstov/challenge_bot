from tgbot.utils import get_telebot
from telebot import types
from telebot.handler_backends import State, StatesGroup  # States
from telebot import custom_filters
from tgbot.keyboards.new_exercise_kb import miss_description_kb, measurement_kb

bot = get_telebot()


class AddExerciseState(StatesGroup):
    name = State()
    description = State()
    measurement = State()


@bot.message_handler(commands='cansel', state='*')
def new_exercise(message):
    bot.send_message(message.chat.id, "Отменяем")
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(commands='new', state='*')
def new_exercise_name(message):
    bot.send_message(message.chat.id, "Создаём новое упражнение!\n Введите его название:")
    bot.set_state(message.from_user.id, AddExerciseState.name, message.chat.id)


@bot.message_handler(state=AddExerciseState.name)
def new_exercise_description(message):
    bot.send_message(message.chat.id, "Введите описание", reply_markup=miss_description_kb)
    bot.set_state(message.from_user.id, AddExerciseState.description, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text

# todo не работает гад как надо.
@bot.callback_query_handler(func=lambda c: c.data == 'miss_description')
def miss_callback(call: types.CallbackQuery):
    bot.set_state(call.message.from_user.id, AddExerciseState.measurement, call.message.chat.id)
    bot.get_state(call.message.from_user.id, call.message.chat.id)
    bot.send_message(call.message.chat.id, "Пропустили. Как будем измерять?", reply_markup=measurement_kb)
    bot.answer_callback_query(call.id)


@bot.message_handler(state=AddExerciseState.description)
def new_exercise_measurement(message):
    bot.send_message(message.chat.id, "Как будем измерять?", reply_markup=measurement_kb)
    bot.set_state(message.from_user.id, AddExerciseState.measurement, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['description'] = message.text


@bot.message_handler(state=AddExerciseState.measurement)
def new_exercise_measurement(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['measurement'] = message.text
        # todo сохранение в БД
        msg = str(data)
        bot.send_message(message.chat.id, msg)
    bot.delete_state(message.from_user.id, message.chat.id)


bot.add_custom_filter(custom_filters.StateFilter(bot))
# bot.add_custom_filter(custom_filters.IsDigitFilter())
