from pydantic import BaseModel
from typing import Optional,List


class Respone(BaseModel):
    msg: Optional[str]
    status: int = 200


class UserBase(BaseModel):
    u_phone:str
    u_name:str


class UserCreate(UserBase):
    u_password:str
    u_registered:str


class UserLogin(BaseModel):
    u_password:str
    u_phone:str


class UserLoginResponse(UserBase):
    token:str


class UserSetUp(UserBase):
    u_password: str
    u_gender:str='male'
    u_level:int=0
    is_active: bool

class User(UserSetUp):
    u_id: int

    class Config:
        orm_mode = True



