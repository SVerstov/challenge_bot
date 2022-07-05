from aiogram import types, Dispatcher
from server import services
from asgiref.sync import sync_to_async


# start
async def start(message: types.Message):
    await message.reply("Стартуем!")
    await sync_to_async(services.add_user, thread_sensitive=True)(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        language_code=message.from_user.language_code
    )


# @dp.message_handler()
async def bad_command(message: types.Message):
    await message.reply("Нет такой команды :(")


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(bad_command)
