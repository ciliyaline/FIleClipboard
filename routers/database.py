from sqlalchemy import create_engine
from .models.base import *
from sqlalchemy.orm import sessionmaker

# TODO: 根据草案换成 PostgreSQL / MS SQL Server
engine = create_engine("sqlite:///./phase_one.db")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

