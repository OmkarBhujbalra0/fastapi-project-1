from sqlalchemy import Column,String,Integer,DATETIME
from database import Base

class ItemDB(Base):
    __tablename__ = "lostfound_table"

    id = Column(Integer,primary_key=True,autoincrement=True)
    item_name = Column(String,nullable=False)
    location = Column(String,nullable=False)
    date_lost_or_found = Column(DATETIME,nullable=False)
    date_reported = Column(DATETIME,nullable=False)
    status = Column(String,nullable=False)

class Users(Base):
    __tablename__ = 'userstable'

    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String,unique=True,nullable=False)
    hashed_password = Column(String,nullable=False)