from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters


def book_event(update: Update, context: CallbackContext):
    update.message.reply_text("Iltimos, tadbirni bron qilish uchun kerakli ma'lumotlarni kiriting:")
    return "BOOKING"

