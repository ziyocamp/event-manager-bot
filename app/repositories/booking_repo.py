from app.database import SessionLocal

from app.models.booking import Booking


def create_booking(db: SessionLocal, user_id: int, event_id:int, ticket_id: int):
    booking = Booking(user_id=user_id, event_id=event_id, ticket_id=ticket_id)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

def get_bookings_by_user_id(db: SessionLocal, user_id: int):
    return db.query(Booking).filter(Booking.user_id == user_id).all()
