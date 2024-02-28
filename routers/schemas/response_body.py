from pydantic import BaseModel

# 这里没用到 orm_mode, 因为响应体所有属性被手动赋值
# 称不上是多好的实现吧, 只希望运行没有问题

class FileResponseBody(BaseModel):
    id: str
    filename: str
    filesize: str
    hash: str       # 那这个只可能是外链了
    createdAt: str  # 这个应该是何时生成
    expiresIn: int
    encrypted: bool
    hashedPassword: str