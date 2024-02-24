from .base import Base

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship



# 可按上传时间, 文件类型, 文件名排序等, 这些要添加索引
class Item:
    id = mapped_column(Integer, primary_key=True)
    hashed_passwd = mapped_column(String)
    upload_time = mapped_column(String, index=True)
    life_cycle = mapped_column(int)
    MAX_LIFE_CYCLE: int = 7 * 24 * 3600 # second

    owner_id = mapped_column(Integer, ForeignKey("users.id"))



class Text(Base, Item):
    __tablename__ = "text"
    content = mapped_column(String)
    title = mapped_column(String, index=True)
    description = mapped_column(String, default="")
    type = mapped_column(String, index=True, default="text")    # optional, e.g. cpp, js, ...
    length = mapped_column(Integer)

    owner = relationship("users", back_populates="text")

    MAX_LENGTH: int = 65536 # temporary


class File(Base, Item):
    __tablename__ = "file"
    content = mapped_column(String) # 本意是云存储的外链, 可能没时间实现
    filename = mapped_column(String, index=True)
    type = mapped_column(String, index=True)
    size = mapped_column(Integer)

    owner = relationship("users", back_populates="file")

    # FIXME: 这个是单个用户的总存储量, 不应该写在这里
    # MAX_SIZE = 1 * 1024 * 1024 * 1024 # 1gb -> byte


