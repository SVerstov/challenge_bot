import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv('TG_API_TOKEN')
HOST = os.getenv('HOST').rstrip('/')


def register_webhook():
    response = requests.get(
        f'https://api.telegram.org/bot{API_TOKEN}/setWebhook?url={HOST}/telegram/callback'
    )
    print("Запуск бота:", response.status_code, response.text)


if __name__ == '__main__':
    register_webhook()
