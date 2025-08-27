from telegram import Update
from telegram.ext import ConversationHandler,CallbackContext, Dispatcher, MessageHandler, Filters, CallbackQueryHandler

from app.database import SessionLocal
from app.models import user
from app.models.user import User, RoleEnum

from app.config import change_name_states, change_role_states

from app.repositories.user_repo import get_user_by_telegram_id, update_user_full_name
from app.repositories.booking_repo import get_bookings_by_user_id
from app.bot.keyboards.settings import get_change_user_role_keyboard, get_confirm_role_keyboard, change_name_keyboard, get_settings_keyboard, get_change_user_role_keyboard, get_change_user_info_keyboard

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


def send_user_tickets(update: Update, context: CallbackContext):
    with SessionLocal() as db:
        user = get_user_by_telegram_id(db, update.effective_user.id)
        if not user:
            start(update, context)
            return

        bookings = get_bookings_by_user_id(db, user.id)
        if not bookings:
            update.message.reply_text("Sizda hech qanday bron mavjud emas.")
            return

        booking_list = []
        for booking in bookings:
            booking_list.append(f"Event: {booking.ticket.event.title}, Ticket: {booking.ticket.ticket_type}")

        update.message.reply_text("Sizning bronlaringiz:\n" + "\n".join(booking_list))


def send_change_user_info(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Malumotlaringizni o'zgartirish uchun quyidagi ma'lumotlarni kiriting:",
        reply_markup=get_change_user_info_keyboard()
    )


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


def send_role_change(update: Update, context: CallbackContext):
    session = SessionLocal()
    user = get_user_by_telegram_id(session, update.effective_user.id)
    if not user:
        start(update, context)
        return

    update.message.reply_text("Yangi rolni tanlang:", reply_markup=get_change_user_role_keyboard(user))
    return change_role_states.ENTER_ROLE


def enter_role(update: Update, context: CallbackContext):
    session = SessionLocal()
    user = get_user_by_telegram_id(session, update.effective_user.id)
    if not user:
        start(update, context)
        return

    context.user_data['new_role'] = update.callback_query.data.split(":")[1]
    update.callback_query.message.reply_text(f"Rolingiz {context.user_data['new_role']} deb o'zgartirilsinmi?", reply_markup=get_confirm_role_keyboard(user))
    return change_role_states.CONFIRM_ROLE


def confirm_role_change(update: Update, context: CallbackContext):
    session = SessionLocal()
    user = get_user_by_telegram_id(session, update.effective_user.id)
    if not user:
        start(update, context)
        return

    user.role = RoleEnum(context.user_data['new_role'])
    session.commit()
    update.callback_query.message.reply_text(f"Rolingiz {user.role.value} deb o'zgartirildi.")

    return ConversationHandler.END


def cancel_role_change(update: Update, context: CallbackContext):
    update.callback_query.message.reply_text("Rolni o'zgartirish bekor qilindi.")

    context.user_data.clear()
    return ConversationHandler.END


def register(dispatcher: Dispatcher):
    dispatcher.add_handler(MessageHandler(Filters.text("⚙️ Sozlamalar"), send_settings))
    dispatcher.add_handler(MessageHandler(Filters.text("🛒 Mening bookinglarim"), send_user_tickets))
    dispatcher.add_handler(MessageHandler(Filters.text("Ma'lumotlarimni o'zgartirish"), send_change_user_info))

    conversation_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text("Roli o'zgartirish"), send_role_change)],
        states={
            change_role_states.ENTER_ROLE: [
                CallbackQueryHandler(enter_role, pattern="^set_role:Tashkilotchi$|^set_role:User$")
            ],
            change_role_states.CONFIRM_ROLE: [
                CallbackQueryHandler(confirm_role_change, pattern="set_role:confirm"),
                CallbackQueryHandler(cancel_role_change, pattern="set_role:cancel")
            ]
        },
        fallbacks=[MessageHandler(Filters.text("Bekor qilish"), send_settings)],
    )
    dispatcher.add_handler(conversation_handler)

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
