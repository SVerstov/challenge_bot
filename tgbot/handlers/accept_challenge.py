from telebot import types
from tgbot.create_bot import bot

from tgbot.utils import get_or_save_user
from server.models import Challenges, ExerciseSet
from django.db.models import Q
from tgbot.keyboards.all_challenges_kb import get_pick_challenge_kb


@bot.message_handler(commands=['accept'])
def start_challenge(message: types.Message):
    user = get_or_save_user(message)
    if user.challenge_accepted:
        bot.send_message(message.from_user.id, f'У вас уже есть принятый челлендж - *{user.challenge_accepted.name}*')
        # todo клавиатура с возможностью сброса
    else:
        challenge_list = Challenges.objects.filter(Q(owner_id=message.from_user.id) | Q(for_all=True))
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
                             f'\nДлительность челленджа: {challenge.duration} дней'
            kb = get_pick_challenge_kb(challenge.name, challenge.id)
            bot.send_message(message.from_user.id, challenge_info, reply_markup=kb)




