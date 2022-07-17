from django.apps import AppConfig
import logging
import sys
from telebot import logger as tlogger


class ServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'server'

    def ready(self):
        super(ServerConfig)
        from tgbot import handlers

