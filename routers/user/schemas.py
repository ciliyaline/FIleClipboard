from pydantic import BaseModel,EmailStr
from typing import Union

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
    
class UserBase(BaseModel):
    email:EmailStr = None
class UserCreate(UserBase):
    password: str
    
# 用户模型
class User(UserBase):
    id: int
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None
    # role:str = None
    
    class Config:
        orm_mode = True

class UserInDB(User):
    hashed_password: str