from pydantic import BaseModel

# 本意 Item, Text, File 是用作 response_model 的
# 但是和数据约定配合不是很好, 导致完全没用上
# 重构的事还是下次一定吧
# upd: Item,Text,File 添加后缀 Out, 本来 Create 应是对应的单词 In
# 重构下次一定

class ItemBase(BaseModel):
    http_id: str
    upload_time: str
    lift_cycle: int
    owner_id: int

class ItemCreate(ItemBase):
    passwd: str         # 这里其实是 hashed_password, 加密已在 .router 里完成

class ItemOut(ItemBase):
    id: int

    class Config:
        orm_mode = True


class TextBase(ItemBase):
    content: str
    title: str = ""
    description: str = ""
    type: str = ""
    length: int

class TextCreate(TextBase, ItemCreate):
    pass

class TextOut(TextBase, ItemOut):
    pass


class FileBase(ItemBase):
    address: str
    filename: str
    type: str
    size: int

class FileCreate(FileBase, ItemCreate):
    pass

class FileOut(FileBase, ItemOut):
    pass