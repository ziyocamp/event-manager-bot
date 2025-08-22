import enum

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import relationship

from app.database import Base


class EventStatus(enum.Enum):
    upcoming = "upcoming"
    ongoing = "ongoing"
    completed = "completed"
    cancelled = "cancelled"


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(String, nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    location = Column(String(250), nullable=True)

    organizer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(EventStatus), default=EventStatus.upcoming, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    organizer = relationship("User", back_populates="events")
    tickets = relationship("Ticket", back_populates="event", cascade="all, delete")
