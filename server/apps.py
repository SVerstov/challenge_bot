from django.apps import AppConfig
import logging



class ServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'server'

    def ready(self):
        super(ServerConfig)
        from tgbot import handlers

