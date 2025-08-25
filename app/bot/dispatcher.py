from telegram.ext import Updater

from app.config import settings
from app.bot.handlers import start, settings as settings_handler, help as help_handler


def run_bot():
    updater = Updater(token=settings.BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start.register(dispatcher)
    settings_handler.register(dispatcher)
    help_handler.register(dispatcher)

    updater.start_polling()
    updater.idle()
