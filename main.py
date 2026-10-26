from fastapi import FastAPI,HTTPException,Depends
from datetime import datetime
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from database import get_db,engine,Base
import models
from models import ItemDB
app = FastAPI()

Base.metadata.create_all(bind=engine)

class Lost_Found(BaseModel):
    item_name: str
    location: str
    date: datetime = Field(default_factory=datetime.now)
    date_reported: datetime = Field(default_factory=datetime.now)
    status: str

@app.get('/')
def home():
    return {"message":"Welcome to Lost and Found Portal."}

lost_and_found_list = []

@app.get('/items')
def display(db:Session = Depends(get_db)):
    item_data = db.query(ItemDB).all()
    return item_data

@app.get('/items/{item_name}')
def search(item_name:str,db:Session = Depends(get_db)):
    item_data = db.query(ItemDB).filter(ItemDB.item_name == item_name).first()
    if not item_data:
        raise HTTPException(status_code=404,detail="Item not found in database.")
    return item_data
@app.post('/items')
def adds(item:Lost_Found,db:Session = Depends(get_db)):
    item_data = ItemDB(item_name=item.item_name,location=item.location,date_lost_or_found=item.date,status=item.status,date_reported=item.date_reported)
    db.add(item_data)
    db.commit()
    db.refresh(item_data)
    return {"message":"Item Added Successfully."}