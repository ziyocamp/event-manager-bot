from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime, func, CheckConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    ticket_type = Column(String(50), nullable=False)   # e.g. "VIP", "Standard"
    price = Column(Numeric(10, 2), CheckConstraint("price >= 0"), nullable=False, default=0) # check positive value
    quantity = Column(Integer, CheckConstraint("quantity >= 0"), nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    event = relationship("Event", back_populates="tickets")
    bookings = relationship("Booking", back_populates="ticket", cascade="all, delete")
