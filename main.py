from fastapi import FastAPI,HTTPException,Depends
from datetime import datetime
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from database import get_db,engine,Base
import models
from models import ItemDB
app = FastAPI()
from typing import Literal

Base.metadata.create_all(bind=engine)

class Lost_Found(BaseModel):
    item_name: str
    location: str
    date: datetime = Field(default_factory=datetime.now)
    date_reported: datetime = Field(default_factory=datetime.now)
    status: Literal["lost","found"]

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

@app.put('/items/{item_id}')
def update(item_id:int,new_item:Lost_Found,db:Session = Depends(get_db)):
    item_data = db.query(ItemDB).filter(ItemDB.id == item_id).first()

    if not item_data:
        raise HTTPException(status_code=404,detail="Item not found in Database.")

    item_data.item_name = new_item.item_name
    item_data.date_lost_or_found = new_item.date
    item_data.location = new_item.location
    item_data.status = new_item.status

    db.commit()
    db.refresh(item_data)
    return {"message":"Item Updated Successfully","data":item_data}

@app.delete('/items/{item_id}')
def removes(item_id:int,db:Session = Depends(get_db)):
    item_data = db.query(ItemDB).filter(ItemDB.id == item_id).first()

    if not item_data:
        raise HTTPException(status_code=404, detail="Item not found in Database.")

    db.delete(item_data)
    db.commit()
    return {"message":"Item removed successfully."}