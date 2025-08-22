from telegram import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu_keyboard():
    keyboard = [
        [KeyboardButton("📅 Eventlar"), KeyboardButton("🛒 Mening bookinglarim")],
        [KeyboardButton("ℹ️ Yordam")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
