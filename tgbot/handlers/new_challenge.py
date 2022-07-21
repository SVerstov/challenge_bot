from telebot import types
from telebot.handler_backends import State, StatesGroup

from server.models import ExercisesAll, Challenges, ExerciseSet
from tgbot.keyboards.exercises_kb import get_exercises_kb
from tgbot.keyboards.challenges_kb import miss_description_kb, offer_to_finish
from tgbot.create_bot import bot


class NewChallengeState(StatesGroup):
    name = State()
    description = State()
    duration = State()
    choose_exercise = State()
    save_exercise = State()
    save_all = State()


@bot.message_handler(commands=['new_challenge'])
def set_challenge_name(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Создаём новый спортивный челлендж!\n Введите его название:")
    bot.set_state(chat_id, NewChallengeState.name)
    bot.add_data(chat_id, owner=chat_id)
    bot.add_data(chat_id, added_exercises={})
    # TODO проверка-что такое упражнение уже есть


@bot.message_handler(state=NewChallengeState.name)
def set_challenge_duration(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Введите описание или нажмите 'Пропустить'", reply_markup=miss_description_kb)
    bot.set_state(chat_id, NewChallengeState.description)
    bot.add_data(chat_id, name=message.text)


@bot.callback_query_handler(func=lambda c: c.data == 'miss_description', state=NewChallengeState.description)
def miss_description(call: types.CallbackQuery):
    call.message.text = ''
    bot.answer_callback_query(call.id)
    set_challenge_description(call.message)


@bot.message_handler(state=NewChallengeState.description)
def set_challenge_description(message: types.Message):
    chat_id = message.chat.id
    bot.add_data(chat_id, description=message.text)
    bot.send_message(chat_id, "Введите продолжительность челленджа (в днях):")
    bot.set_state(chat_id, NewChallengeState.duration)


@bot.message_handler(state=NewChallengeState.duration)
def choose_exercise(message: types.Message):
    chat_id = message.chat.id
    if not is_positive_integer(message.text):
        bot.send_message(chat_id, "Введите положительное число, без букв:")
    else:
        bot.add_data(chat_id, duration=int(message.text))
        show_exercise_kb(chat_id)


def show_exercise_kb(chat_id):
    kb = get_exercises_kb(chat_id)
    bot.send_message(chat_id, "Выберите упражнение из списка:", reply_markup=kb)
    bot.set_state(chat_id, NewChallengeState.choose_exercise)


@bot.callback_query_handler(func=lambda c: c.data.isdigit(), state=NewChallengeState.choose_exercise)
def exercise_chosen(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    exercise = ExercisesAll.objects.get(pk=int(call.data))
    measurement = exercise.get_measurement_display()
    bot.add_data(chat_id, current_exercise=exercise)
    bot.send_message(chat_id,
                     f'Какое количество упражнения \'*{exercise.name}*\' ({measurement}) необходимо сделать?')
    bot.set_state(chat_id, NewChallengeState.save_exercise)
    bot.answer_callback_query(call.id)


@bot.message_handler(state=NewChallengeState.save_exercise)
def save_exercise(message: types.Message):
    chat_id = message.chat.id
    if message.text.isdigit() and int(message.text) >= 0:
        with bot.retrieve_data(chat_id) as data:
            exercise: ExercisesAll = data['current_exercise']
            data['added_exercises'][exercise.id] = (exercise, int(message.text))

            if int(message.text) == 0:
                del data['added_exercises'][exercise.id]

        # make a clear string for response
        if data['added_exercises']:
            exercises_info = '\n'.join(
                [f'*{x[0].name}*:  {x[1]} {(x[0].get_measurement_display())}' for x in
                 data['added_exercises'].values()]) \
                             + f'\n\n Длительность челленджа: {data["duration"]} дней' \
                               f'\n`Чтобы отредактировать упражнение, выберите его повторно.`' \
                               f'\n`Для удаления упражнения, установите количество равным 0. `'

            bot.send_message(chat_id,
                             f"Уже выбраны следующие упражнения:\n\n{exercises_info}", reply_markup=offer_to_finish)
            bot.set_state(chat_id, NewChallengeState.save_all)
        else:
            exercises_info = 'Нет упражнений 🤕'
            bot.send_message(chat_id, exercises_info)
            show_exercise_kb(chat_id)


    else:
        bot.send_message(chat_id, "Введите положительное число, без букв")


@bot.callback_query_handler(func=lambda c: c.data in ['add_exercise', 'finish'], state=NewChallengeState.save_all)
def exercise_chosen(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    if call.data == 'add_exercise':
        bot.answer_callback_query(call.id)
        show_exercise_kb(chat_id)
    elif call.data == 'finish':
        with bot.retrieve_data(chat_id) as data:
            save_new_challenge(data)
            bot.send_message(chat_id, f'Новый Челлендж \'{data["name"]}\' сохранён!')
        bot.delete_state(chat_id)


def is_positive_integer(text: str) -> bool:
    return text.strip().isdigit() and int(text) > 0


@bot.message_handler(state=NewChallengeState.save_all)
@bot.message_handler(state=NewChallengeState.choose_exercise)
def inline_mistake(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Ошибка, используйте кнопки!')


def save_new_challenge(data: dict):
    challenge_obj = Challenges.objects.create(
        owner_id=data['owner'],
        name=data['name'],
        description=data['description'],
        duration=data['duration'],
    )

    for exercise_id in data['added_exercises']:
        exercise = data['added_exercises'][exercise_id][0]
        amount = data['added_exercises'][exercise_id][1]
        if exercise.measurement == 'minutes':
            amount *= 60
        ExerciseSet.objects.create(
            challenge_id=challenge_obj.id,
            name=exercise.name,
            amount=amount,
            measurement=exercise.measurement,
        )
