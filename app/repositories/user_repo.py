from sqlalchemy.orm import Session

from app.models.user import User, RoleEnum


def get_user_by_telegram_id(db: Session, telegram_id: int):
    return db.query(User).filter(User.telegram_id == telegram_id).first()


def create_user(db: Session, telegram_id: int, username: str, full_name: str):
    user = User(
        telegram_id=telegram_id,
        username=username,
        full_name=full_name,
        role=RoleEnum.user
    )    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
