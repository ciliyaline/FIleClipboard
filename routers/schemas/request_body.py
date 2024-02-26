from pydantic import BaseModel
# prototype from https://static.lnkkerst.me/open/ot-2024winter-pastebin/latest.json
# 其实是写完 xxxCreate 才发现 api 接口已经写好了(我的我的)
# 这里相当于再加一层接口

class TextRequestBody(BaseModel):
    content: str
    expiresIn: int  # second
    encrypted: bool
    password: str


class FileRequestBody(BaseModel):
    filename: str
    file: str       # binary
    password: str
    encrypted: int  # 是否加密，非 0 为加密. 至于为什么这里 int 上面 bool, 数据约定是这样写的
    expiresIn: int  # second