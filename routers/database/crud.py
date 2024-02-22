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

def encrypt(passwd: str) -> str:
    # FIXME
    return passwd

def commit(db: Session, item: models.Item) -> models.Item:
    # 不知道 db.add() 是根据什么判断提交到哪张表的,
    # 啊, 我傻了, session 应该本身就包含了自己是哪张表的信息
    # TODO: 正式跑起来之后有机会可以试试这个函数, 不知道能不能用
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def create_user(db: Session, user: schemas.UserCreate) -> models.Users:
    db_user: models.Users = models.Users(
        id = user.id,
        hashed_passwd = encrypt(user.passwd),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_text(db: Session, t: schemas.TextCreate) -> models.Text:
    # TODO: 也许有办法从子类构建父类(TextCreate -> TextBase)
    db_text : models.Text = models.Text(
        id = t.id,
        hashed_passwd = encrypt(t.passwd),
        upload_time = "tmp", # FIXME
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
    db_file : models.Text = models.Text(
        id = f.id,
        hashed_passwd = encrypt(f.passwd),
        upload_time = "tmp", # FIXME
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

# update


































