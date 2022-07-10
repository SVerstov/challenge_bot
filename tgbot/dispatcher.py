from tgbot.handlers.info_services import send_text, send_help_info
from tgbot.utils import get_user, Bot



from telebot.handler_backends import State, StatesGroup  # States



def test(message):
    Bot.reply_to(message, "Test is ok!")





class AddExerciseStates(StatesGroup):
    name = State()
    description = State()
    measurement = State()


# AddExerciseState.

def dispatch(data: dict) -> None:
    # user = get_user_from_telegram(data, 'message')
    #


    if 'message' in data:
        telegram_id = data['message']['from']['id']
        text = data['message'].get('text', None)
        # if text and AddExerciseState.status():
        #     AddExerciseState.finish()
        #     # add_exercise(telegram_id, text, AddExerciseState)
        if text:
            match text:
                case '/start':
                    get_user(data)
                    send_text(telegram_id, 'Стартуууууем!')
                case '/help':
                    send_help_info(telegram_id)
                case 'add_exercise' | '/add_exercise' | 'добавить упражнение':
                    pass
                case 'fsm' | '/fsm':
                    send_text(telegram_id, 'Введите название упражнения!')
                case _:
                    send_text(telegram_id, 'Непонятная команда')
