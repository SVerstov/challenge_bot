import os

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from .handlers import register_handlers


storage = MemoryStorage()
TOKEN = os.getenv('TG_API_TOKEN')
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)


async def on_startup(dp: Dispatcher):
    register_handlers(dp)
    print('Бот запустился!')


def run_pooling():
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
