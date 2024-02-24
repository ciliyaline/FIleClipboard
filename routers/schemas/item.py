from pydantic import BaseModel

class ItemBase(BaseModel):
    upload_time: str

class ItemCreate(ItemBase):
    passwd: str

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