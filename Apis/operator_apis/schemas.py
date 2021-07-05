from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    u_phone:str
    u_gender:str
    u_name:str


class UserCreate(UserBase):
    u_password:str
    u_registered:str
    u_level:int


class User(UserBase):
    u_id: int
    is_active: bool

    class Config:
        orm_mode = True