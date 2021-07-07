from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    u_phone:str
    u_name:str


class UserCreate(UserBase):
    u_password:str
    u_registered:str


class UserSetUp(UserBase):
    u_gender:str='male'
    u_level:int=0
    is_active: bool

class User(UserSetUp):
    u_id: int

    class Config:
        orm_mode = True



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    phone: Optional[str]