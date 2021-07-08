from fastapi import APIRouter
from typing import List

from fastapi import Depends,  HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db

from Apps.Users_router import schemas,models
from Apps.Users_router.dependencies import User
from ..dependencies.database import engine


models.Base.metadata.create_all(bind=engine)


user_app = APIRouter(tags=["API for Users"],
                prefix="/API")


@user_app.get('/')
async def hello():
    return {"hello": "demo_router"}


@user_app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = User.get_user_by_phone(db, user.u_phone)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return User.create_user(db=db, user=user)


@user_app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = User.get_users(db, skip=skip, limit=limit)
    return users

