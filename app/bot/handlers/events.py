from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, MessageHandler, Filters, Dispatcher, CallbackQueryHandler

from app.database import SessionLocal
from app.repositories.event_repo import get_all_events, get_event_by_id


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = []
    if header_buttons:
        menu.append(header_buttons)
    for i in range(0, len(buttons), n_cols):
        menu.append(buttons[i:i + n_cols])
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def send_events(update: Update, context: CallbackContext):
    with SessionLocal() as db:
        events = get_all_events(db)

    if not events:
        update.message.reply_text("Sizda hech qanday event yo'q.")
        return

    event_list = []
    for event in events:
        event_list.append([
            InlineKeyboardButton(event.title, callback_data=f"event:{event.id}")
        ])

    reply_markup = InlineKeyboardMarkup(event_list)
    update.message.reply_text("Bu yerda eventlar ro'yxati:", reply_markup=reply_markup)


def send_event_details(update: Update, context: CallbackContext):
    event_id = context.match.group(1)
    print(event_id)
    with SessionLocal() as db:
        event = get_event_by_id(db, event_id)
        if not event:
            update.callback_query.message.reply_text("Event topilmadi.")
            return
        
        event_status_map = {
            "upcoming": "Kutilmoqda",
            "ongoing": "Davom etmoqda",
            "completed": "Tamomlangan"
        }

        update.callback_query.message.reply_text(
            f"Event tafsilotlari:\n{event.title}\n{event.description}" \
            f"\nBoshlanish vaqti: {event.start_time}\nTugash vaqti: {event.end_time}\n" \
            f"Manzil: {event.location}\n" \
            f"Tashkilotchi: {event.organizer.full_name}\n" \
            f"Status: {event_status_map.get(event.status.value, event.status.value)}"
        )


def register(dispatcher: Dispatcher):
    dispatcher.add_handler(MessageHandler(Filters.text("📅 Eventlar"), send_events))
    dispatcher.add_handler(CallbackQueryHandler(send_event_details, pattern=r"^event:(\d+)$"))
