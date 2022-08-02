from tgbot.create_bot import bot


# all commands must reset bot state
@bot.middleware_handler(update_types=['message'])
def middleware_test(bot_instance, message):
    a = message
    if message.content_type == 'text':
        if message.text.startswith('/') and not message.text in ['/cansel', '/stats']:
            bot.delete_state(message.from_user.id)
