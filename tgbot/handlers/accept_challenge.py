from telebot import types
from tgbot.create_bot import bot

from tgbot.utils import get_or_save_user
from server.models import Challenges, AcceptedChallenges
from django.db.models import Q



@bot.message_handler(commands=['accept'])
def start_challenge(message: types.Message):
    user = get_or_save_user(message)
    if user.challenge_accepted:
        bot.send_message(message.from_user.id, f'У вас уже есть принятый челлендж - *{user.challenge_accepted.name}*')
        # todo клавиатура с возможностью сброса
    else:
        challenge_list = Challenges.objects.filter(Q(owner_id=message.from_user.id) | Q(for_all=True))

        for challenge in challenge_list:
            # challenge: Challenges
            bot.send_message(message.from_user.id, '')




