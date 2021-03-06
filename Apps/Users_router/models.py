from sqlalchemy import Boolean, Column, Integer, String

from ..dependencies.database import Base


class User(Base):
    __tablename__ = "Users"

    u_id            = Column(Integer, primary_key=True, autoincrement=True)
    u_name          = Column(String, default="admin")
    u_phone         = Column(String, unique=True, index=True)
    u_gender        = Column(String, default="male")
    u_password      = Column(String)
    u_registered    = Column(String, default=None)
    u_level         = Column(Integer,default=0)
    is_active       = Column(Boolean, default=True)