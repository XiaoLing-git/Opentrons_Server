from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime
import datetime

from ..database import Base


class User(Base):
    __tablename__ = "operators"

    u_id            = Column(Integer, primary_key=True, index=True)
    u_phone         = Column(String, unique=True, index=True)
    u_gender        = Column(String, unique=True, index=True)
    u_password      = Column(String)
    u_registered    = Column(String, default=None)
    u_level         = Column(Integer)
    is_active       = Column(Boolean, default=True)