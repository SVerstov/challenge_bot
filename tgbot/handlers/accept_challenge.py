from django.forms import model_to_dict
from telebot import types
from telebot.handler_backends import StatesGroup, State

from tgbot.create_bot import bot

from tgbot.utils import get_or_save_user, get_today_date
from server.models import Challenges, ExerciseSet, AcceptedChallenges, AcceptedExerciseSet
from django.db.models import Q
from tgbot.keyboards.all_challenges_kb import get_pick_challenge_kb, reset_kb
from tgbot.keyboards.counter_kb import counter_stats_kb


class AcceptChallengeState(StatesGroup):
    choose = State()


@bot.message_handler(commands=['accept'])
def start_challenge(message: types.Message):
    chat_id = message.from_user.id
    user = get_or_save_user(message)
    bot.set_state(chat_id, AcceptChallengeState.choose)
    if user.challenge_accepted:
        bot.send_message(chat_id,
                         f'У вас уже есть принятый челлендж - *{user.challenge_accepted.name}*',
                         reply_markup=reset_kb)
    else:
        challenge_list = Challenges.objects.filter(Q(owner_id=chat_id) | Q(for_all=True))
        exercise_list = ExerciseSet.objects.all()

        for challenge in challenge_list:
            exercises = exercise_list.filter(challenge_id=challenge.id)
            exercises_info = ''

            description = '\n' + challenge.description if challenge.description else ''
            for exercise in exercises:
                exercises_info += f'*{exercise.name}*: {exercise.amount}  {exercise.get_measurement_display()}\n'
            challenge_info = f'*{challenge.name}*' \
                             f'`{description}`' \
                             f'\n\n{exercises_info}' \
                             f'\nДлительность челленджа: *{challenge.duration}* дней'
            # todo ДЕНЬ ДНЯ ДНЕЙ - в зависимости от числа
            kb = get_pick_challenge_kb(challenge.name, challenge.id)
            bot.send_message(chat_id, challenge_info, reply_markup=kb)
        bot.send_message(chat_id,"Ничего не подходит?\n/"
                                 "Создайте свои упражнения /new_exercise\n"
                                 "и челленджи /new_challenge", parse_mode='HTML')




@bot.callback_query_handler(func=lambda c: c.data == 'reset_challenge', state=AcceptChallengeState.choose)
def cansel_challenge(call: types.CallbackQuery):
    chat_id = call.from_user.id
    user = get_or_save_user(call.message)
    user.challenge_accepted.delete()
    bot.answer_callback_query(call.id)
    bot.send_message(chat_id, 'Прогресс сброшен!')


@bot.callback_query_handler(func=lambda c: True, state=AcceptChallengeState.choose)
def save_accepted_challenge(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    user = get_or_save_user(call.message)

    challenge = Challenges.objects.get(pk=int(call.data))
    kwargs = model_to_dict(challenge, exclude=['id', 'owner', 'for_all'])
    date_start = get_today_date(user.time_zone)
    accepted_challenge = AcceptedChallenges.objects.create(**kwargs, date_start=date_start)
    accepted_challenge.save()
    user.challenge_accepted = accepted_challenge
    user.save()

    for exercise in challenge.exerciseset_set.all():
        kwargs = model_to_dict(exercise, exclude=['id', 'challenge'])
        accepted_exercise = AcceptedExerciseSet.objects.create(challenge_id=accepted_challenge.id, **kwargs)
        accepted_exercise.save()

    bot.send_message(chat_id, '💪 Вызов принят! 💪\n'
                              'Для учёта используйте команду /counter', reply_markup=counter_stats_kb)
    bot.answer_callback_query(call.id, '>> CHALLENGE ACCEPTED <<')
    bot.delete_state(call.from_user.id)
