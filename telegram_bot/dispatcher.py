from telegram_bot.services.info_services import send_text, send_help_info
from telegram_bot.utils import get_user_from_telegram, get_telebot
from telegram_bot.keyboards.test_keyboard import inline_kb

bot = get_telebot()






def dispatch(data: dict) -> None:
    # user = get_user_from_telegram(data, 'message')
    # todo ?? зачем при каждом сообщении делать запрос в бд?

    if 'message' in data:
        telegram_id = data['message']['from']['id']
        if text := data['message'].get('text', None):

            match text:
                case '/start':
                    get_user_from_telegram(data)
                    send_text(telegram_id, 'Стартуууууем!', reply_markup=inline_kb)
                case '/help':
                    send_help_info(telegram_id)

                case _:
                    send_text(telegram_id, 'Непонятная команда')


