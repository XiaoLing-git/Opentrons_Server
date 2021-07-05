from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    u_phone:str
    u_gender:str


class UserCreate(UserBase):
    u_password:str
    u_registered:str
    u_level:int


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True