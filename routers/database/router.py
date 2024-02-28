from time import time
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

# from routers.database.crud import generate_storage_address, store_file    # vscode 自动生成, 如果相对路径有问题可以试试

from .database import get_db    # TODO:不过这样一来, 数据库表会创建吗, 好像并不会
from .crud import *
from ..schemas import *
from .. import models

def get_current_time() -> str:
    return str(time())


def encrypt(passwd: str) -> str:
    return "passwd" # TODO: 以后应该是从别的地方借一个 encrypt()


def get_filename_suffix(filename: str) -> str:
    index: int = filename.rfind(".")
    if index == -1:
        return ""
    else:
        return filename[index:]


def generate_http_id() -> str:
    return "http_id-" + get_current_time()


def generate_download_link(file: models.File) -> str:
    # TODO:我想到一个绝妙的解决方法, 生成下载链接类似 httpid, 然后加到一个 map 里, ...
    return "download_link"


# TODO: 可以考虑做成 Item 的成员函数
def expired(item: models.Item) -> bool:
    return float(item.upload_time) + item.life_cycle < float(get_current_time())


router = FastAPI()


# 草案没写查询参数 user_id, 请求体里也没有, 但是必须有
@router.post("/p/")
async def router_create_text(body: TextRequestBody, user_id: int, db: Session = Depends(get_db)) -> None:
    text_create: TextCreate = TextCreate(
        http_id=generate_http_id(),
        upload_time=get_current_time(),
        lift_cycle=body.expiresIn,
        owner_id=user_id,
        passwd=encrypt(body.password) if body.encrypted else "",
        content=body.content,   # NOTE:就先假设是合法数据
        length=len(body.content),
    )
    # NOTE:如果每个用户文本数量有限制, 应在此处审查
    create_text(db, text_create)


@router.get("/p/{id}")
async def get_text_content(id: str, db: Session = Depends(get_db)) -> str:
    text_in_db: models.Text | None = get_text_by_http_id(db, id)

    if text_in_db is None:
        raise HTTPException(404, "resource not found")
    if expired(text_in_db):
        raise HTTPException(410, "resource expired")

    return text_in_db.content


@router.get("/f/", response_model=FileResponseBody)  # 数据约定这里是 get, 没写错
async def router_create_file(body: FileRequestBody, user_id: int, db: Session = Depends(get_db)) -> FileResponseBody:
    timestmap: str = get_current_time()
    http_id: str = generate_http_id()
    file_address: str = generate_storage_address(http_id)
    store_file(file_address, body.file)
    file_size: int = len(body.file)
    hashed_passwd: str = encrypt(body.password) if body.encrypted else ""

    file_create: FileCreate = FileCreate(
        http_id=http_id,
        upload_time=timestmap,
        lift_cycle=body.expiresIn,
        owner_id=user_id,
        passwd=hashed_passwd,
        address=file_address,
        filename=body.filename,
        type=get_filename_suffix(body.filename),
        size=file_size,
    )
    # TODO: 这里应该查询用户剩余容量, 等待交接
    create_file(db, file_create)

    return FileResponseBody(
        id=http_id,
        filename=body.filename,
        filesize=str(file_size),
        hash="",        # FIXME
        createdAt=timestmap,
        expiresIn=body.expiresIn,
        encrypted=(body.encrypted != 0),
        hashedPassword=hashed_passwd,
    )


@router.get("/f/{id}", response_model=FileResponseBody)
async def get_file_info(id: str, db: Session = Depends(get_db)) -> FileResponseBody:
    file: models.File | None = get_file_by_http_id(db, id)

    if file is None:
        raise HTTPException(404, "resource not found")
    if expired(file):
        raise HTTPException(410, "resource expired")

    return FileResponseBody(
        id=id,
        filename=file.filename,
        filesize=file.size,
        hash=generate_download_link(file),
        createdAt=file.upload_time,
        expiresIn=file.life_cycle,
        encrypted=(file.hashed_passwd != ""),
        hashedPassword=file.hashed_passwd,
    )


# NOTE: 这个函数应该绑定一个一次性(?), 有时效(?)的链接
@router.get("/fake_download_link/", response_model=StreamingResponse)
async def router_get_file() -> StreamingResponse:
    file_address: str = ""
    return StreamingResponse(file_address)