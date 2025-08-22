from telegram import Update
from telegram.ext import ConversationHandler,CallbackContext, Dispatcher, MessageHandler, Filters, CallbackQueryHandler

from app.database import SessionLocal
from app.models import user
from app.models.user import User, RoleEnum

from app.config import change_name_states

from app.repositories.user_repo import get_user_by_telegram_id, update_user_full_name
from app.bot.keyboards.settings import change_user_role_keyboard, change_name_keyboard, get_settings_keyboard

from app.bot.handlers.start import start


def send_settings(update: Update, context: CallbackContext):
    session = SessionLocal()

    try:
        user: User | None = get_user_by_telegram_id(session, update.effective_user.id)
        if not user:
            start(update, context)
            return

    except Exception as e:
        update.message.reply_text("Xatolik yuz berdi.")
        return

    finally:
        session.close()

    settings_message = f"{user.full_name} sizning sozlamalaringiz"

    if user.role == RoleEnum.admin:
        settings_message += "\n- Siz adminsiz. Barcha huquqlarga egasiz."
    if user.role == RoleEnum.organizer:
        settings_message += "\n- Siz tashkilotchisiz. Eventlarni boshqarish huquqiga egasiz."
    if user.role == RoleEnum.user:
        settings_message += "\n- Siz foydalanuvchisiz. Faqat o'z eventlaringizni ko'rishingiz mumkin."

    update.message.reply_text(settings_message, reply_markup=get_settings_keyboard())


def change_name(update: Update, context: CallbackContext):
    update.message.reply_text("Ismingizni kiriting:")
    return change_name_states.ENTER_NAME


def set_name(update: Update, context: CallbackContext):
    context.user_data['full_name'] = update.message.text

    update.message.reply_text(f"Ismingiz {context.user_data['full_name']} deb o'gartirilsinmi?", reply_markup=change_name_keyboard())
    return change_name_states.CONFIRM_NAME


def confirm_name(update: Update, context: CallbackContext):
    full_name = context.user_data.get('full_name')
    session = SessionLocal()
    try:
        update_user_full_name(session, update.effective_user.id, full_name)
        update.callback_query.message.reply_text(f"Ismingiz {full_name} deb o'zgartirildi.")

    except Exception as e:
        print(e)
        session.rollback()
        update.callback_query.message.reply_text("Xatolik yuz berdi.")
    finally:
        session.close()

    context.user_data.clear()
    return ConversationHandler.END


def cancel_name_change(update: Update, context: CallbackContext):
    update.callback_query.message.reply_text("Ismni o'zgartirish bekor qilindi.")

    context.user_data.clear()
    return ConversationHandler.END


def register(dispatcher: Dispatcher):
    dispatcher.add_handler(MessageHandler(Filters.text("⚙️ Sozlamalar"), send_settings))

    conversation_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text("Ismni o'zgartirish"), change_name)],
        states={
            change_name_states.ENTER_NAME: [
                MessageHandler(Filters.text, set_name)
            ],
            change_name_states.CONFIRM_NAME: [
                CallbackQueryHandler(confirm_name, pattern="^change_name:confirm$"),
                CallbackQueryHandler(cancel_name_change, pattern="^change_name:cancel$")
            ]
        },
        fallbacks=[MessageHandler(Filters.text("Bekor qilish"), send_settings)],
    )
    dispatcher.add_handler(conversation_handler)
