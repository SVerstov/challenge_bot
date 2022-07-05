import os, django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'challenge_bot.settings')
django.setup()

from telegram_bot.bot_main import run_pooling


if __name__ == "__main__":
    run_pooling()