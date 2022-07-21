from telebot import types
from telebot.types import InlineKeyboardButton as Ibtn
from server.models import ExercisesAll
from django.db.models import Q


def get_exercises_kb(telegram_id: int, for_all=True) -> types.InlineKeyboardMarkup:
    if for_all:
        exercises = ExercisesAll.objects.filter(Q(owner_id=telegram_id) | Q(for_all=True))
    else:
        exercises = ExercisesAll.objects.filter(owner_id=telegram_id)
    user_exercises_kb = types.InlineKeyboardMarkup()
    user_exercises_kb.max_row_keys = 3
    exercise_btns = [Ibtn(exercises.name, callback_data=exercises.id) for exercises in exercises]
    user_exercises_kb.row(*exercise_btns)
    return user_exercises_kb
