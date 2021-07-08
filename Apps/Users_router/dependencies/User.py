from sqlalchemy.orm import Session
from .. import models,schemas
from fastapi import Header
from ...dependencies.database import redis_instance


def get_user_by_phone(db: Session, phone: str):
    return db.query(models.User).filter(models.User.u_phone == phone).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.u_password
    db_user = models.User(u_phone=user.u_phone,
                          u_password=fake_hashed_password,
                          u_name =user.u_name,
                          u_registered = user.u_registered)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user




def verify_token_access(admin_phone:str,token:str = Header(None)):
    token_in_redis = redis_instance.get(admin_phone)
    if token_in_redis is None:
        return (False,None)
    if token == token_in_redis.decode():
        return (True,admin_phone)
    return (False,None)