from fastapi.routing import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from routers.database import get_db
from .schemas import User
from ..database import Users

router = APIRouter()

@router.post("/register/")
async def register(user: User, db: Session = Depends(get_db)):
    db_user = Users(id=user.id, passwd=user.passwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/get/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(Users).filter(Users.id == user_id).first()
