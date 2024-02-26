from fastapi import Depends, FastAPI, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from .database import get_db    # TODO:不过这样一来, 数据库表会创建吗, 好像并不会
from .crud import *
from ..schemas import *

def get_current_time() -> str:
    pass    # TODO


def encrypt(passwd: str) -> str:
    pass    # TODO: 以后应该是从别的地方借一个 encrypt()


def get_filename_suffix(filename: str) -> str:
    index: int = filename.rfind(".")
    if index == -1:
        return ""
    else:
        return filename[index:]


def spawn_http_id() -> str:
    pass


router = FastAPI()


# 草案没写参查询数 user_id, 请求体里也没有, 但是必须有
@router.post("/p/")
async def router_create_text(body: TextRequestBody, user_id: int, db: Session = Depends(get_db)) -> None:
    text_create: TextCreate = TextCreate(
        http_id=spawn_http_id(),
        upload_time=get_current_time(),
        lift_cycle=body.expiresIn,
        owner_id= user_id,
        passwd=encrypt(body.password) if body.encrypted else "",
        content=body.content,   # NOTE:就先假设是合法数据
        length=len(body.content),
    )
    # NOTE:如果每个用户文本数量有限制, 应在此处审查
    create_text(db, text_create)


@router.get("/p/{id}")
async def get_text(id: str) -> str:
    pass


@router.get("/f/", response_model=FileResponseBody)  # 数据约定这里是 get, 没写错
async def router_create_file(body: FileRequestBody, user_id: int, db: Session = Depends(get_db)) -> FileResponseBody:
    file_create: FileCreate = FileCreate(
        http_id=spawn_http_id(),
        upload_time=get_current_time(),
        lift_cycle=body.expiresIn,
        owner_id= user_id,
        passwd=encrypt(body.password) if body.encrypted else "",
        content=body.file,
        filename=body.filename,
        type=get_filename_suffix(body.filename),
        size=len(body.file),
    )
    # TODO: 这里应该查询用户剩余容量
    create_file(db, file_create)


@router.get("/f/{id}", response_model=FileResponseBody)
async def get_file(id: str) -> FileResponseBody:
    pass