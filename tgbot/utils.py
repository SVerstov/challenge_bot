import datetime
from datetime import timedelta

import telebot.types
from telebot import types

from server.models import AcceptedExerciseSet, Challenges, ExerciseSet, ExercisesAll, User
from django.db.models import F, Q
from server.models import User
from tgbot.create_bot import bot
from tgbot.keyboards.challenges_kb import get_pick_challenge_kb, get_delete_challenge_kb
from tgbot.settings import list_of_commands


def get_user_by_id(telegram_id):
    return User.objects.filter(telegram_id=telegram_id).first()


def get_or_save_user(message: types.Message) -> User:
    telegram_id = message.chat.id
    user = User.objects.filter(telegram_id=telegram_id).first()
    if not user:
        user = create_user(message)
    return user


def create_user(message):
    telegram_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    language_code = message.from_user.language_code
    user = User.objects.create(telegram_id=telegram_id,
                               username=username,
                               first_name=first_name,
                               last_name=last_name,
                               language_code=language_code)
    return user


def seconds_to_mmss(seconds: int or float) -> str:
    return str(datetime.timedelta(seconds=int(seconds))).lstrip('0:')


def get_exercise_progress_info(exercise: AcceptedExerciseSet, today: bool = True, percent: bool = False,
                               timezone: int = 3) -> str:
    if exercise.measurement == 'minutes':
        if exercise.progress:
            progress_info = seconds_to_mmss(exercise.progress)
        else:
            progress_info = 0
        amount_info = str(exercise.amount / 60) + ' мин'
        progress_on_last_day = seconds_to_mmss(exercise.progress_on_last_day)

        info = f'*{exercise.name}:*\n' \
               f' {progress_info} из {amount_info}'

    else:
        progress_info = f'{exercise.progress:g}'
        amount_info = str(exercise.amount)
        progress_on_last_day = f'{exercise.progress_on_last_day:g}'

        info = f'*{exercise.name}:*\n' \
               f' {progress_info} {exercise.get_measurement_display().lower()} из {amount_info}'

    if today and exercise.last_day != get_today_date(timezone):
        progress_on_last_day = 0

    if today:
        info += f' | Сегодня: {progress_on_last_day}'
    if percent:
        info += f' | Прогресс: {get_exercise_progress_percentage(exercise, excess=True):g}%'  #
    return info


def get_exercise_progress_percentage(exercise: AcceptedExerciseSet, excess=False) -> float:
    percentage = (exercise.progress / exercise.amount) * 100
    if not excess:
        if percentage > 100:
            percentage = 100
    return round(percentage, 1)


def get_today_date(timezone: int):
    """ :returns current date considering UTC timezone"""
    offset = datetime.timedelta(hours=timezone)
    tz = datetime.timezone(offset, name='тест')
    return datetime.datetime.now(tz=tz).date()


def is_challenge_finished(user):
    unfinished_exercises = user.challenge_accepted.acceptedexerciseset_set.filter(progress__lt=F('amount'))
    if not unfinished_exercises:
        return True
    return False


def show_all_challenges(chat_id: int, action: str):
    """ Shows all challenges
     :param action 'pick' or 'delete'
     """
    if action not in ('pick', 'delete'):
        raise AttributeError('param "action must be "pick" or "delete"')

    if action == 'pick':
        challenge_list = Challenges.objects.filter(Q(owner_id=chat_id) | Q(for_all=True))
    else:
        challenge_list = Challenges.objects.filter(owner_id=chat_id)

    exercise_list = ExerciseSet.objects.filter(challenge__in=challenge_list)
    for challenge in challenge_list:
        exercises = exercise_list.filter(challenge_id=challenge.id)
        exercises_info = ''

        description = '\n' + challenge.description if challenge.description else ''
        for exercise in exercises:
            if exercise.measurement == 'minutes':
                amount = exercise.amount / 60
            else:
                amount = exercise.amount

            exercises_info += f'*{exercise.name}*: {amount:g}  {exercise.get_measurement_display()}\n'
        duration = challenge.duration
        challenge_info = f'*{challenge.name}*' \
                         f'`{description}`' \
                         f'\n\n{exercises_info}' \
                         f'\nДлительность челленджа: *{duration}*  {get_form_of_day(duration)}'

        if action == 'pick':
            kb = get_pick_challenge_kb(challenge.name, challenge.id)
        else:
            kb = get_delete_challenge_kb(challenge.name, challenge.id)
        bot.send_message(chat_id, challenge_info, reply_markup=kb)


def get_exercise_list_as_text(chat_id: int) -> str:
    exercises = ExercisesAll.objects.filter(Q(owner_id=chat_id) | Q(for_all=True))
    return '\n'.join(exercise.name for exercise in exercises)


def set_up_commands(telegram_id: int, language_code: str) -> None:
    if language_code in ['ukr', 'bel']:
        language_code = 'ru'
    elif language_code not in list_of_commands:
        language_code = 'en'
    commands = list_of_commands[language_code]
    bot.set_my_commands(
        commands=[telebot.types.BotCommand(cmd, description) for cmd, description in commands.items()],
        scope=telebot.types.BotCommandScopeChat(telegram_id))


def delete_object(chat_id, object):
    object_name = object.name
    object.delete()
    bot.send_message(chat_id, f'{object_name}- удалено 🚫')


def get_form_of_day(num):
    if num % 10 == 1:
        return 'день'
    elif num % 10 in (2, 3, 4):
        return 'дня'
    else:
        return 'дней'


def get_timezone(chat_id: int) -> int:
    try:
        with bot.retrieve_data(chat_id) as data:
            timezone = data['timezone']
            return timezone
    except KeyError:
        user = get_user_by_id(chat_id)
        timezone = user.time_zone
        return timezone


def finish_check(chat_id):
    user = get_user_by_id(chat_id)
    if is_challenge_finished(user):
        info = make_info_text(user)
        bot.send_message(chat_id, info, parse_mode='Markdown')
        bot.send_message(chat_id, f'😎 Вы террррминаторрр! Челенж пройден 🏋🏼‍♂️')
        user.challenge_accepted.delete()
        bot.delete_state(chat_id)


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

    common_info = f'*{challenge_name}* ({duration} {get_form_of_day(duration)})\n\n' \
                  f'Дата старта: {date_start.strftime("%d.%m.%y")}\n' \
                  f'Дата окончания: {date_end.strftime("%d.%m.%y")} \n\n' \
                  f'Сегодня *{number_of_today}* день. \n' \
                  f'Общий прогресс *{overall_progress:g}*% 🚀\n' \
                  f'Желательный прогресс *{ideally_progress:g}*%\n\n'

    return common_info + all_exercises_info
