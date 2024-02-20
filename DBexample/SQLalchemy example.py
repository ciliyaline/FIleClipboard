from sqlalchemy import create_engine
from sqlalchemy import Integer, String
from sqlalchemy.orm import sessionmaker, mapped_column, DeclarativeBase

from getpass import getpass



engine = create_engine("sqlite:///./example.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # close the connection after the request is finished

db_session = next(get_db())
class Base(DeclarativeBase):
    pass
class User(Base):
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key=True)
    passwd = mapped_column(String)
Base.metadata.create_all(bind=engine)

username1 = int(input("Enter username: "))
password1 = getpass("Enter password: ")


db_session.add(User(id=username1, passwd=password1))
db_session.commit() 
db_session.query(User).all()
print(db_session.query(User).filter(User.id == username1).first().passwd)

