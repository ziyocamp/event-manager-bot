from app.database import SessionLocal
from app.models.event import Event
from app.models.ticket import Ticket


def get_all_events(db: SessionLocal):
    return db.query(Event).all()

def get_event_by_id(db: SessionLocal, event_id: int):
    return db.query(Event).filter(Event.id == event_id).first()

def get_ticket_by_id(db: SessionLocal, ticket_id: int):
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()
