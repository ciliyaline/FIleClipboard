from pydantic import BaseModel

class ItemBase(BaseModel):
    http_id: str
    upload_time: str
    lift_cycle: int
    owner_id: int

class ItemCreate(ItemBase):
    passwd: str         # 这里其实是 hashed_password, 加密已在 .router 里完成

class Item(ItemBase):   # 收到请求时, 从数据库读出来并返回的东西
    id: int

    class Config:
        orm_mode = True


class TextBase(ItemBase):
    content: str
    title: str
    description: str
    type: str
    length: int

class TextCreate(TextBase, ItemCreate):
    pass

class Text(TextBase, Item):   # 收到请求时, 从数据库读出来并返回的东西
    pass


class FileBase(ItemBase):
    content: str
    filename: str
    type: str
    size: int

class FileCreate(FileBase, ItemCreate):
    pass

class File(FileBase, Item): # 收到请求时, 从数据库读出来并返回的东西
    pass