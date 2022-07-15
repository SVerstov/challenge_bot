from telebot import types
from telebot.types import InlineKeyboardButton as Ibtn
from telebot.types import KeyboardButton as Btn
from server.models import ExercisesAll
from django.db.models import Q

miss_description_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
miss_description_kb.add(
    Btn('/Пропустить описание'),
    Btn('/cansel')
)

measurement_kb = types.InlineKeyboardMarkup()
measurement_kb.row(
    Ibtn('В штуках', callback_data='numbers'),
    Ibtn('В километрах', callback_data='distance'),
    Ibtn('В минутах', callback_data='minutes'),
)

offer_to_finish = types.InlineKeyboardMarkup()
offer_to_finish.row(
    Ibtn('Добавить упражнение 💪', callback_data='add_exercise'),
    Ibtn('Завершить 🏆', callback_data='finish'),
)


def get_exercises_kb(telegram_id: int, add_done_btn: bool = False) -> types.InlineKeyboardMarkup:
    exercises = ExercisesAll.objects.filter(Q(owner_id=telegram_id) | Q(for_all=True))

    user_exercises_kb = types.InlineKeyboardMarkup()
    user_exercises_kb.max_row_keys = 3
    exercise_btns = [Ibtn(exercises.name, callback_data=exercises.id) for exercises in exercises]
    user_exercises_kb.row(*exercise_btns)
    if add_done_btn:
        user_exercises_kb.add(Ibtn('✅  Готово ✅', callback_data='done'))
    return user_exercises_kb
