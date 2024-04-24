from .base import Base

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship


LIFE_CYCLE: int = 7 * 24 * 3600 # 或可考虑置为静态成员


# 如果不能用继承, 就单独写 text.py 和 file.py
# 可按上传时间, 文件类型, 文件名排序等, 这些要添加索引
class Item(Base):
    __tablename__ = "item"
    id = mapped_column(Integer, primary_key=True)
    hashed_password = mapped_column(String)
    upload_time = mapped_column(String, index=True)

    owner_id = mapped_column(Integer, ForeignKey("users.id"))

    # owner = relationship("users", back_populates="item")  # 这个在子类里单独写


class Text(Item):
    __tablename__ = "text"
    content = mapped_column(String)
    item_id = Column(Integer, ForeignKey('item.id'))
    title = mapped_column(String, index=True)
    description = mapped_column(String, default="")
    type = mapped_column(String, index=True, default="text")    # optional, e.g. cpp, js, ...
    length = mapped_column(Integer)

    owner = relationship("users", back_populates="text")
    item = relationship("Item", back_populates="text")
    
    MAX_LENGTH: int = 65536 # temporary


class File(Item):
    __tablename__ = "file"
    content = mapped_column(String) # 本意是云存储的外链, 可能没时间实现
    file_id = mapped_column(Integer, primary_key=True)
    filename = mapped_column(String, index=True)
    type = mapped_column(String, index=True)
    size = mapped_column(Integer)

    owner_id = Column(Integer, ForeignKey('users.id'), name="file_owner_id")  
    owner = relationship("User", back_populates="files")  
    item_id = Column(Integer, ForeignKey('item.id'), name="item_owner_id")  
    item = relationship("Item", back_populates="files")

    # FIXME: 这个是单个用户的总存储量, 不应该写在这里
    # MAX_SIZE = 1 * 1024 * 1024 * 1024 # 1gb -> byte


