from .base import Base

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import mapped_column
class Users(Base):
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key=True)
    hashed_passwd = mapped_column(String)