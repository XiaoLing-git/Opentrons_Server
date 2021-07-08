from sqlalchemy.orm import Session

from .. import models,schemas


def get_user_by_phone(db: Session, phone: str):
    return db.query(models.User).filter(models.User.u_phone == phone).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.u_password
    db_user = models.User(u_phone=user.u_phone, u_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user