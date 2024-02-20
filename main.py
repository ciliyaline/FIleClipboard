from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from contextlib import asynccontextmanager
from pydantic import BaseModel
from datetime import datetime
import databases
import sqlalchemy
import os

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 打印数据库连接URL
print("DATABASE_URL:", os.getenv("DATABASE_URL"))

# 创建 FastAPI 应用程序
app = FastAPI()

# 创建数据库连接
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("No database URL provided. Please set the DATABASE_URL environment variable.")

database = databases.Database(DATABASE_URL)

# 创建数据库表
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("username", sqlalchemy.String, unique=True, index=True),
    sqlalchemy.Column("password", sqlalchemy.String),
)

texts = sqlalchemy.Table(
    "texts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("content", sqlalchemy.Text),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime)
)

# 密码哈希
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2密码流
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 用户模型
class User(BaseModel):
    username: str

# 获取当前用户
async def get_current_user(token: str = Depends(oauth2_scheme)):
    query = users.select().where(users.c.username == token)
    user = await database.fetch_one(query)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# 用户注册
@app.post("/register/", response_model=User)
async def register_user(username: str, password: str, database: databases.Database = Depends(get_current_user)):
    query = users.insert().values(username=username, password=pwd_context.hash(password))
    user_id = await database.execute(query)
    return {"username": username}

# 用户登录
@app.post("/token/")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), database: databases.Database = Depends(get_current_user)):
    query = users.select().where(users.c.username == form_data.username)
    user = await database.fetch_one(query)
    if not user or not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user["username"], "token_type": "bearer"}

# 文本暂存
@app.post("/store-text/")
async def store_text(content: str, current_user: User = Depends(get_current_user)):
    query = texts.insert().values(content=content, created_at=datetime.now())
    await database.execute(query)
    return {"message": "Text stored successfully"}

# 创建数据库表
async def create_tables():
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)

# 关闭应用程序时关闭数据库连接
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.disconnect()
    await database.connect()
    await create_tables()
