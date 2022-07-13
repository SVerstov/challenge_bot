from telebot import types
from telebot.handler_backends import State, StatesGroup

from server.models import Challenges, Exercise, CurrentChallenge
from tgbot.keyboards.user_create import get_exercises_kb, offer_to_finish
from tgbot.create_bot import bot


class NewChallengeState(StatesGroup):
    description = State()
    duration = State()
    exercises = State()
    save_exercise = State()
    save_all = State()


@bot.message_handler(commands=['new_challenge'])
def set_challenge_name(message: types.Message):
    bot.send_message(message.chat.id, "Создаём новый спортивный челлендж!\n Введите его название:")
    bot.set_state(message.from_user.id, NewChallengeState.description)
    bot.add_data(message.from_user.id, creator_id=message.from_user.id)


@bot.message_handler(state=NewChallengeState.description)
def set_challenge_duration(message: types.Message):
    bot.send_message(message.chat.id, "Введите описание:")
    bot.set_state(message.from_user.id, NewChallengeState.duration)
    bot.add_data(message.from_user.id, name=message.text)


@bot.message_handler(state=NewChallengeState.duration)
def set_challenge_description(message: types.Message):
    bot.send_message(message.chat.id, "Введите продолжительность челленджа (в днях):")
    bot.set_state(message.from_user.id, NewChallengeState.exercises)
    bot.add_data(message.from_user.id, description=message.text)


@bot.message_handler(state=NewChallengeState.exercises)
def choose_exercise(message: types.Message):
    if not is_positive_integer(message.text):
        bot.send_message(message.chat.id, "Введите положительное число, без букв:")
    else:
        kb = get_exercises_kb(message.chat.id)
        bot.send_message(message.chat.id, "Выберите упражнение из списка:", reply_markup=kb)
        bot.set_state(message.chat.id, NewChallengeState.exercises)
        bot.add_data(message.chat.id, duration=int(message.text))
        bot.add_data(message.chat.id, added_exercises={})


@bot.callback_query_handler(func=lambda c: c.data.isdigit(), state=NewChallengeState.exercises)
def exercise_chosen(call: types.CallbackQuery):
    exercise = Exercise.objects.get(pk=int(call.data))
    measurement = exercise.get_measurement_display()
    bot.add_data(call.message.chat.id, current_exercise=exercise)
    bot.send_message(call.message.chat.id, f'Введите цель для упражнения *{exercise.name}* ({measurement}):')
    bot.set_state(call.message.chat.id, NewChallengeState.save_exercise)
    bot.answer_callback_query(call.id)


@bot.message_handler(state=NewChallengeState.save_exercise)
def save_exercise(message: types.Message):
    if message.text.isdigit() and int(message.text) >= 0:
        with bot.retrieve_data(message.chat.id) as data:
            exercise = data['current_exercise']
            data['added_exercises'][exercise.id] = (exercise.name, int(message.text))
            if int(message.text) == 0:
                del data['added_exercises'][exercise.id]

        # make a clear string for response
        if data['added_exercises']:
            exercises_info = '\n'.join([f'*{x[0]}*:  {str(x[1])}' for x in data['added_exercises'].values()])
        else:
            exercises_info = 'Нет упражнений 🤕'

        bot.send_message(message.chat.id,
                         f"Уже выбраны следующие упражнения:\n{exercises_info}",
                         reply_markup=offer_to_finish)
        bot.set_state(message.chat.id, NewChallengeState.exercises)
    else:
        bot.send_message(message.chat.id, "Введите положительное число, без букв")


@bot.callback_query_handler(func=lambda c: c.data in ['add_exercise', 'finish'], state=NewChallengeState.exercises)
def exercise_chosen(call: types.CallbackQuery):
    if call.data == 'add_exercise':
        kb = get_exercises_kb(call.message.chat.id)
        bot.send_message(call.message.chat.id, "Выберите упражнение из списка:", reply_markup=kb)
    elif call.data == 'finish':
        with bot.retrieve_data(call.message.chat.id) as data:
            save_new_challenge(data)

    bot.answer_callback_query(call.id)


def is_positive_integer(text: str) -> bool:
    return text.strip().isdigit() and int(text) > 0


def save_new_challenge(data: dict):
    challenge_obj = Challenges.objects.create(
                                            creator_id=data['creator_id'],
                                            main_copy = True,
                                            name=data['name'],
                                            description=data['description'],
                                            duration= data['duration'],
                                            )

    for exercise_id in data['added_exercises'].keys():
        save2 = CurrentChallenge.objects.create(
                                            challenge_id=challenge_obj.id,
                                            exercise_id=exercise_id,
                                            exercises_amount=data['added_exercises'][exercise_id][1],
                                            )
    return 'ok'


def test_save():
    exercise = Exercise.objects.get(pk=33)    
    data = {'creator_id': 403196518, 'name': 'Test2', 'description': 'Странный Челлендж', 'duration': 50,
     'added_exercises': {28: ('Отжимания', 5000), 29: ('Подтягивания', 7000), 30: ('Бег', 4)}, 'current_exercise'
     : exercise}
    save_new_challenge(data)