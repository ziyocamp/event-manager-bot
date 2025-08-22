from telegram.ext import Updater

from app.config import settings
from app.bot.handlers import start


def run_bot():
    updater = Updater(token=settings.BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start.register(dispatcher)

    updater.start_polling()
    updater.idle()
