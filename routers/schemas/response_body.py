from pydantic import BaseModel

# 这里没用到 orm_mode, 因为响应体所有属性被手动赋值
# 称不上是多好的实现吧, 只希望运行没有问题

class FileResponseBody(BaseModel):
    id: str
    filename: str
    filesize: str
    hash: str       # whats this?
    createdAt: str  # 这个应该是生成的外链
    expiresIn: int
    encrypted: bool
    hashedPassword: str