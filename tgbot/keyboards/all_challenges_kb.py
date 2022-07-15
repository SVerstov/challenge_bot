from telebot import types
from telebot.types import InlineKeyboardButton as Ibtn
from telebot.types import KeyboardButton as Btn
from server.models import Challenges
from django.db.models import Q

def get_all_challenges_kb(telegram_id: int) -> types.InlineKeyboardMarkup:
    challemges = Challenges.objects.filter(Q(owner_id=telegram_id) | Q(for_all=True))

    all_challenges_kb = types.InlineKeyboardMarkup()
    all_challenges_kb.max_row_keys = 3