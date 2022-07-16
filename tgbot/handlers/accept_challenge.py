from django.forms import model_to_dict
from telebot import types
from telebot.handler_backends import StatesGroup, State

from tgbot.create_bot import bot

from tgbot.utils import get_or_save_user
from server.models import Challenges, ExerciseSet, AcceptedChallenges, AcceptedExerciseSet
from django.db.models import Q
from tgbot.keyboards.all_challenges_kb import get_pick_challenge_kb, reset_kb


class AcceptChallengeState(StatesGroup):
    choose = State()


@bot.message_handler(commands=['accept'])
def start_challenge(message: types.Message):
    chat_id = message.from_user.id
    user = get_or_save_user(message)
    if user.challenge_accepted:
        bot.send_message(chat_id,
                         f'У вас уже есть принятый челлендж - *{user.challenge_accepted.name}*',
                         reply_markup=reset_kb)
    else:
        challenge_list = Challenges.objects.filter(Q(owner_id=chat_id) | Q(for_all=True))
        exercise_list = ExerciseSet.objects.all()

        for challenge in challenge_list:
            # challenge: Challenges

            exercises = exercise_list.filter(challenge_id=challenge.id)
            exercises_info = ''
            for exercise in exercises:
                exercises_info += f'*{exercise.name}*: {exercise.amount}  {exercise.get_measurement_display()}\n'
            challenge_info = f'*{challenge.name}*' \
                             f'\n`{challenge.description}`' \
                             f'\n\n{exercises_info}' \
                             f'\nДлительность челленджа: *{challenge.duration}* дней'
            # todo ДЕНЬ ДНЯ ДНЕЙ - в зависимости от числа
            kb = get_pick_challenge_kb(challenge.name, challenge.id)
            bot.send_message(chat_id, challenge_info, reply_markup=kb)
    bot.set_state(chat_id, AcceptChallengeState.choose)


@bot.callback_query_handler(func=lambda c: c.data == 'reset_challenge', state=AcceptChallengeState.choose)
def cansel_challenge(call: types.CallbackQuery):
    chat_id = call.from_user.id
    user = get_or_save_user(call)
    user.challenge_accepted.delete()

    bot.answer_callback_query(call.id, 'Прогресс сброшен!')


@bot.callback_query_handler(func=lambda c: True, state=AcceptChallengeState.choose)
def save_accepted_challenge(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    challenge = Challenges.objects.get(pk=int(call.data))

    kwargs = model_to_dict(challenge, exclude=['id', 'owner', 'for_all'])
    accepted_challenge = AcceptedChallenges.objects.create(**kwargs)
    accepted_challenge.save()
    user = get_or_save_user(call)
    user.challenge_accepted = accepted_challenge
    user.save()

    for exercise in challenge.exerciseset_set.all():
        kwargs = model_to_dict(exercise, exclude=['id', 'challenge'])
        accepted_exercise = AcceptedExerciseSet.objects.create(challenge_id=accepted_challenge.id, **kwargs)
        accepted_exercise.save()

    bot.answer_callback_query(call.id, '>> CHALLENGE ACCEPTED <<')
    bot.delete_state(call.from_user.id)