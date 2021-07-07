from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException,status

from . import models, schemas
from ..database import SessionLocal


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


SECRET_KEY = "dfaae6d94b90367f8bb4ef984d26c15d0aa11797d95bfa644706ba20c4dd683e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.u_id == user_id).first()


def get_user_by_phone(db: Session, phone: str):
    return db.query(models.User).filter(models.User.u_phone == phone).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(u_phone=user.u_phone,
                          u_password=user.u_password,
                          u_registered=user.u_registered,
                          u_name=user.u_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate(db:Session, phone:str, password:str):
    user = get_user_by_phone(db,phone)
    if not user:
        return False
    if not verify_password(password, user.u_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(phone:str, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        pyload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        token_phone:str = pyload.get('sub')
        if token_phone is None:
            raise credentials_exception
        token_data = schemas.TokenData(token_phone)
    except JWTError:
        raise credentials_exception
    user = get_user_by_phone(db,phone=token_data.phone)
    if user is None:
        return user





