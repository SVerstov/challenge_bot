import os

from telebot import StateMemoryStorage, TeleBot, custom_filters

from tgbot import settings

# CREATE BOT
API_TOKEN = os.getenv('TG_API_TOKEN')
state_storage = StateMemoryStorage()
bot = TeleBot(API_TOKEN, state_storage=state_storage, parse_mode='Markdown', exception_handler=settings.ExceptionHandler())

# FILTERS
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())
bot.add_custom_filter(custom_filters.IsDigitFilter())

