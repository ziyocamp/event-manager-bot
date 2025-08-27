from telegram import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu_keyboard():
    keyboard = [
        [KeyboardButton("📅 Eventlar")],
        [KeyboardButton("ℹ️ Yordam"), KeyboardButton("⚙️ Sozlamalar")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
