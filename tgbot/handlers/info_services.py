from telebot.custom_filters import TextFilter

from tgbot.settings import start_message
from tgbot.utils import get_or_save_user, get_today_date, get_exercise_progress_info, get_exercise_progress_percentage, \
    set_up_commands
from tgbot.create_bot import bot
from server.models import User
from telebot import types
from datetime import timedelta


@bot.message_handler(commands=['cansel'], state='*')
def cansel(message: types.Message):
    chat_id = message.chat.id
    state = bot.get_state(message.from_user.id)
    if state:
        bot.send_message(chat_id, "Отменяем 🚫")
        bot.delete_state(message.from_user.id)
    else:
        bot.send_message(chat_id, "Нечего отменять")


@bot.message_handler(commands=['start', 'help'])
def start_info(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, start_message)
    set_up_commands(telegram_id=message.from_user.id, language_code=message.from_user.language_code)
    get_or_save_user(message)


@bot.message_handler(text=TextFilter(starts_with='/stats', ignore_case=True), state='*')
def show_info(message: types.Message):
    chat_id = message.chat.id
    user = get_or_save_user(message)
    if user.challenge_accepted:
        info = make_info_text(user)
        bot.send_message(chat_id, info, parse_mode='Markdown')
    else:
        bot.send_message(chat_id, "Нет активных челленджей 😢\n"
                                  "Используйте команду /accept чтобы запустить один из них.")


def make_info_text(user: User) -> str:
    challenge_name = user.challenge_accepted.name
    date_start = user.challenge_accepted.date_start
    duration = user.challenge_accepted.duration
    date_end = date_start + timedelta(days=duration)
    today = get_today_date(user.time_zone)
    number_of_today = (today - date_start).days + 1
    ideally_progress = round(100 * number_of_today / duration, 1)
    if ideally_progress > 100:
        ideally_progress = 100

    all_exercises_info = ''
    list_of_progress = []
    exercises = user.challenge_accepted.acceptedexerciseset_set.all()
    for exercise in exercises:
        exercise_info = get_exercise_progress_info(exercise, today=False, percent=True)
        all_exercises_info += exercise_info + '\n'
        list_of_progress.append(get_exercise_progress_percentage(exercise))

    overall_progress = round(sum(list_of_progress) / len(list_of_progress), 1)

    common_info = f'*{challenge_name}* ({duration} дней)\n\n' \
                  f'Дата старта: {date_start.strftime("%d.%m.%y")}\n' \
                  f'Дата окончания: {date_end.strftime("%d.%m.%y")} \n\n' \
                  f'Сегодня *{number_of_today}* день. \n' \
                  f'Общий прогресс *{overall_progress:g}*% 🚀\n' \
                  f'Желательный прогресс *{ideally_progress:g}*%\n\n'

    return common_info + all_exercises_info
