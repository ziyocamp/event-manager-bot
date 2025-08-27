from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters

from app.database import SessionLocal
from app.repositories.user_repo import get_user_by_telegram_id, create_user
from app.bot.keyboards.main_menu import get_main_menu_keyboard


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    telegram_id = user.id
    username = user.username
    full_name = user.full_name

    db = SessionLocal()
    try:
        existing_user = get_user_by_telegram_id(db, telegram_id)
        if not existing_user:
            create_user(db, telegram_id, username, full_name)
            db_message = "✅ Sizning profilingiz yaratildi."
        else:
            db_message = "👋 Siz avval ro‘yxatdan o‘tgan ekansiz."

    finally:
        db.close()

    message = f"Salom, {full_name}!\n{db_message}\n\n"
    message += "Event Manager Botga xush kelibsiz.\nQuyidagi menyudan kerakli bo‘limni tanlang:"

    reply_markup = get_main_menu_keyboard()

    update.message.reply_text(message, reply_markup=reply_markup)


def main_menu(update: Update, context: CallbackContext):
    reply_markup = get_main_menu_keyboard()
    update.message.reply_text("Bosh menu:", reply_markup=reply_markup)


def register(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text("Bosh menu") & ~Filters.command, main_menu))

