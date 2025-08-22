import enum

from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Enum, func
from sqlalchemy.orm import relationship

from app.database import Base


class RoleEnum(enum.Enum):
    user = "User"
    organizer = "Tashkilotchi"
    admin = "Admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(50), nullable=True, index=True)
    full_name = Column(String(120), nullable=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.user, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship example
    events = relationship("Event", back_populates="organizer")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, full_name={self.full_name}, role={self.role})>"
    