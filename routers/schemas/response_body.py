from pydantic import BaseModel

class FileResponseBody(BaseModel):
    id: str
    filename: str
    filesize: str
    hash: str       # whats this?
    createdAt: str  # whats this
    expiresIn: int
    encrypted: bool
    hashedPassword: str