from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, MessageHandler, Filters, Dispatcher, CallbackQueryHandler

from app.database import SessionLocal
from app.repositories.event_repo import get_all_events, get_event_by_id, get_ticket_by_id
from app.repositories.user_repo import get_user_by_telegram_id
from app.repositories.booking_repo import create_booking


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
            f"Status: {event_status_map.get(event.status.value, event.status.value)}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Biletlar", callback_data=f"tickets:{event.id}")]
            ])
        )


def send_tickets(update: Update, context: CallbackContext):
    event_id = context.match.group(1)
    with SessionLocal() as db:
        event = get_event_by_id(db, event_id)

        tickets = event.tickets
        if not tickets:
            update.callback_query.message.reply_text("Biletlar topilmadi.")
            return

        ticket_list = []
        for ticket in tickets:
            ticket_list.append([
                InlineKeyboardButton(f"Ticket #{ticket.ticket_type}", callback_data=f"ticket:{ticket.id}")
            ])

        reply_markup = InlineKeyboardMarkup(ticket_list)
        update.callback_query.message.reply_text("Bu yerda biletlar ro'yxati:", reply_markup=reply_markup)


def send_ticket_info(update: Update, context: CallbackContext):
    ticket_id = context.match.group(1)
    with SessionLocal() as db:
        ticket = get_ticket_by_id(db, ticket_id)
        if not ticket:
            update.callback_query.message.reply_text("Ticket topilmadi.")
            return

        update.callback_query.message.reply_text(
            f"Ticket tafsilotlari:\n{ticket.event.title}\n" \
            f"Narxi: {ticket.price}\n" \
            f"Turi: {ticket.ticket_type}\n" \
            f"Son: {ticket.quantity}",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Ortga", callback_data=f"event:{ticket.event.id}"),
                    InlineKeyboardButton("Xarid qilish", callback_data=f"buy_ticket:{ticket.id}")
                ]
            ])
        )


def buy_ticket(update: Update, context: CallbackContext):
    ticket_id = context.match.group(1)
    with SessionLocal() as db:
        user = get_user_by_telegram_id(db, update.effective_user.id)
        ticket = get_ticket_by_id(db, ticket_id)
        if not ticket or not user:
            update.callback_query.message.reply_text("Ticket yoki foydalanuvchi topilmadi.")
            return

        create_booking(db, user.id, ticket.event.id, ticket.id)
        update.callback_query.message.reply_text(f"Ticket #{ticket.id} xarid qilindi!")


def register(dispatcher: Dispatcher):
    dispatcher.add_handler(MessageHandler(Filters.text("📅 Eventlar"), send_events))
    dispatcher.add_handler(CallbackQueryHandler(send_event_details, pattern=r"^event:(\d+)$"))
    dispatcher.add_handler(CallbackQueryHandler(send_tickets, pattern=r"^tickets:(\d+)$"))
    dispatcher.add_handler(CallbackQueryHandler(send_ticket_info, pattern=r"^ticket:(\d+)$"))
    dispatcher.add_handler(CallbackQueryHandler(buy_ticket, pattern=r"^buy_ticket:(\d+)$"))

