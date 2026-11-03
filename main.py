from fastapi import FastAPI,HTTPException,Depends
from datetime import datetime
from pydantic import BaseModel,Field,ConfigDict
from sqlalchemy.orm import Session
from database import get_db,engine,Base
import models
from models import ItemDB,Users
from security import hashed_password,verify_password,create_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Literal
import jwt
from security import SECRET_KEY
app = FastAPI()

Base.metadata.create_all(bind=engine)

class Item_Out(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    item_name: str
    location: str
    date_lost_or_found: datetime
    date_reported: datetime
    status: Literal["lost","found"]

class Lost_Found(BaseModel):
    item_name: str
    location: str
    date: datetime = Field(default_factory=datetime.now)
    date_reported: datetime = Field(default_factory=datetime.now)
    status: Literal["lost","found"]

bearer_scheme = HTTPBearer()

class User(BaseModel):
    username: str
    password: str

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(credentials.credentials,SECRET_KEY,algorithms=["HS256"])
        username = payload.get('sub')
    except jwt.PyJWTError:
        raise HTTPException(status_code=401,detail="Invalid Token")
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        raise HTTPException(status_code=401,detail="Invalid Token")
    return user

@app.get('/me')
def homepage(current_user: User = Depends(get_current_user)):
    return {"message":f"Welcome {current_user.username}"}

@app.get('/me/items',response_model=list[Item_Out])
def my_items(current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    items = db.query(ItemDB).filter(ItemDB.owner_id == current_user.id).all()
    return items

@app.get('/')
def home():
    return {"message":"Welcome to Lost and Found Portal."}

lost_and_found_list = []

@app.get('/items',response_model=list[Item_Out])
def display(db:Session = Depends(get_db)):
    item_data = db.query(ItemDB).all()
    return item_data

@app.get('/items/{item_name}',response_model=Item_Out)
def search(item_name:str,db:Session = Depends(get_db)):
    item_data = db.query(ItemDB).filter(ItemDB.item_name == item_name).first()
    if not item_data:
        raise HTTPException(status_code=404,detail="Item not found in database.")
    return item_data

@app.post('/items')
def adds(item:Lost_Found,db:Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    item_data = ItemDB(item_name=item.item_name,location=item.location,date_lost_or_found=item.date,status=item.status,date_reported=item.date_reported,owner_id=current_user.id)
    db.add(item_data)
    db.commit()
    db.refresh(item_data)
    return {"message":"Item Added Successfully."}

@app.put('/items/{item_id}')
def update(item_id:int,new_item:Lost_Found,db:Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    item_data = db.query(ItemDB).filter(ItemDB.id == item_id).first()

    if not item_data:
        raise HTTPException(status_code=404,detail="Item not found in Database.")

    if item_data.owner_id != current_user.id:
        raise HTTPException(status_code=403,detail="Action not Allowed.")

    item_data.item_name = new_item.item_name
    item_data.date_lost_or_found = new_item.date
    item_data.location = new_item.location
    item_data.status = new_item.status

    db.commit()
    db.refresh(item_data)
    return {"message":"Item Updated Successfully","data":item_data}

@app.delete('/items/{item_id}')
def removes(item_id:int,db:Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    item_data = db.query(ItemDB).filter(ItemDB.id == item_id).first()

    if not item_data:
        raise HTTPException(status_code=404, detail="Item not found in Database.")

    if item_data.owner_id != current_user.id:
        raise HTTPException(status_code=403,detail="Action not Allowed.")
    
    db.delete(item_data)
    db.commit()
    return {"message":"Item removed successfully."}

@app.post('/register')
def registration(details:User,db:Session =Depends(get_db)):
    existing_user = db.query(Users).filter(Users.username == details.username).first()

    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists.")

    hashed_pwd = hashed_password(details.password)
    user_data = Users(username=details.username,hashed_password=hashed_pwd)
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return {"message":"New User Registered Successfully.",
            "user": {
                "user_id":user_data.id,
                "username":user_data.username
            }}

@app.post('/login')
def login(details:User,db:Session = Depends(get_db)):
    check_user = db.query(Users).filter(Users.username == details.username).first()
    if not check_user:
        raise HTTPException(status_code=401,detail="Invalid Username or Password")
    check_password = verify_password(details.password,check_user.hashed_password)
    if not check_password:
            raise HTTPException(status_code=401,detail="Invalid Username or Password")

    token = create_token(check_user.username)
    return {"access_token":token,"token_type":"bearer"}