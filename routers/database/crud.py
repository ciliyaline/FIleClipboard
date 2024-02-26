from sqlalchemy.orm import Session
from .. import models, schemas

# read

# 为什么不命名成 User 而要命名成 Users.?
def get_user(db: Session, user_id: int) -> models.Users:
    return db.query(models.Users).filter(models.Users.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.Users:
    pass    # we have no email in Users


# 第 skip 页, 每页 limit 个
def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.Users]:
    return db.query(models.Users).offset(skip).limit(limit).all()


def get_text(db: Session, text_id: int) -> models.Text:
    return db.query(models.Text).filter(models.Text.id == text_id).first()


def get_file(db: Session, file_id: int) -> models.File:
    return db.query(models.File).filter(models.File.id == file_id).first()


# create


def create_user(db: Session, user: schemas.UserCreate) -> models.Users:
    db_user: models.Users = models.Users(
        id = user.id,
        hashed_passwd = user.passwd,    # NOTE: item 的密码是在 .router 里加密了, 此处等待交接
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_text(db: Session, t: schemas.TextCreate) -> models.Text:
    db_text: models.Text = models.Text(
        http_id = t.http_id,
        hashed_passwd = t.passwd,
        upload_time = t.upload_time,
        life_cycle = t.lift_cycle,
        owner_id = t.owner_id,
        # ↑ base class member
        content = t.content,
        title = t.title,
        description = t.description,
        type = t.type,
        length = t.length,
    )
    db.add(db_text)
    db.commit()
    db.refresh(db_text)
    return db_text


def create_file(db: Session, f: schemas.FileCreate) -> models.File:
    db_file: models.File = models.File(
        http_id = f.http_id,
        hashed_passwd = f.passwd,
        upload_time = f.upload_time,
        life_cycle = f.lift_cycle,
        owner_id = f.owner_id,
        # ↑ base class member
        content = f.content, # TODO: 把文件存到服务器和生成外链是哪一步要操作的,是这里吗
        filename = f.filename,
        type = f.type,
        size = f.size,
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


# delete
# TODO:定期删除过期 item

# update


































