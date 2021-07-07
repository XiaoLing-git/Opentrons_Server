from datetime import timedelta

from fastapi import APIRouter,status
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm


from . import models, schemas
from . import cruds as crud
from ..database import engine
from .cruds import get_db

models.Base.metadata.create_all(bind=engine)



operator = APIRouter(
    prefix="/operator",
    tags= ["operator API"],
    responses={404:{'msg': 'not found'}},
)


@operator.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_phone(db, phone=user.u_phone)
    if db_user:
        raise HTTPException(status_code=400, detail="phone already registered")
    return crud.create_user(db=db, user=user)


@operator.post("/token", response_model=schemas.Token)
async def login_for_access_token(formdata: OAuth2PasswordRequestForm=Depends(),db: Session = Depends(get_db)):
    user = crud.authenticate(db,formdata.password,formdata.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=crud.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}