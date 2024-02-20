from pydantic import BaseModel

class User(BaseModel):
    id: int
    passwd: str
    