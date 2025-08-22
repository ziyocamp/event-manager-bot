from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from app.models.user import User, RoleEnum


def change_user_role_keyboard(user: User) -> InlineKeyboardMarkup:
    keyboard = []
    if user.role == RoleEnum.user:
        keyboard.append([InlineKeyboardButton("Tashkilotchi", callback_data="set_role:organizer")])
    elif user.role == RoleEnum.organizer:
        keyboard.append([InlineKeyboardButton("User", callback_data="set_role:user")])
    return InlineKeyboardMarkup(keyboard)


def get_settings_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton("Roli o'zgartirish"), KeyboardButton("Ismni o'zgartirish")],
        [KeyboardButton("Orqaga qaytish")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def change_name_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("Ha", callback_data="change_name:confirm")],
        [InlineKeyboardButton("Yo'q", callback_data="change_name:cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)
