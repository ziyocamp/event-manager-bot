from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters, Dispatcher


def send_help(update: Update, context: CallbackContext):
    help_message = (
        "Yordam olish uchun admin bilan bog'laning.\n" \
        "Telegram: @admin_username"
    )
    update.message.reply_text(help_message)


def register(dispatcher: Dispatcher):
    dispatcher.add_handler(MessageHandler(Filters.text("ℹ️ Yordam"), send_help))

