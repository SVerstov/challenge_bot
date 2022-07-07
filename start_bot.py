import os, django
import requests
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv('TG_API_TOKEN')
HOST = os.getenv('HOST').rstrip('/')


def register_webhook():
    response = requests.get(
        f'https://api.telegram.org/bot{API_TOKEN}/setWebhook?url={HOST}/telegram/callback'
    )
    print(response.status_code, response.text)


if __name__ == '__main__':
    register_webhook()


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'challenge_bot.settings')
# django.setup()
#
# from telegram_bot.bot_main import run_pooling
#
#
# if __name__ == "__main__":
#     run_pooling()
