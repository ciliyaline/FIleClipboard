from pydantic import BaseModel
from .item import Item
from ..user.schemas import User as UserCreate


class UserBase(BaseModel):
    id: int

class User(UserBase):
    items: list[Item] = []
    class Config:
        orm_mode = True