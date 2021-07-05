from fastapi import APIRouter
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from starlette.templating import Jinja2Templates
from starlette.requests import Request

from . import models, schemas
from . import cruds as crud
from ..database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="../../templates")

operator = APIRouter(
    prefix="/operator",
    tags= ["operator API"],
    responses={404:{'msg': 'not found'}},
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@operator.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_phone(db, phone=user.u_phone)

    if db_user:
        raise HTTPException(status_code=400, detail="phone already registered")
    return crud.create_user(db=db, user=user)


@operator.get("/users/")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@operator.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@operator.get("/login")
def login(request:Request):
    return templates.TemplateResponse("html/login.html",{"request":request})

