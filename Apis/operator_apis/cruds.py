from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_phone(db: Session, phone: str):
    return db.query(models.User).filter(models.User.u_phone == phone).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    # password = user.u_password
    # db_user = models.User(email=user.email, u_password=fake_hashed_password)
    db_user = models.User(u_phone=user.u_phone,
                          u_password=user.u_password,
                          u_gender=user.u_gender,
                          u_level=user.u_level,
                          u_registered=user.u_registered)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

