from pwdlib import PasswordHash
from dotenv import load_dotenv
import os 
import jwt
from datetime import datetime,timedelta,timezone

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")

password_hash = PasswordHash.recommended()

def hashed_password(password:str) -> str:
    return password_hash.hash((password))

def verify_password(password:str, hashed_pwd:str) -> bool:
    return password_hash.verify(password,hashed_pwd)

def create_token(username:str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload = {"sub":username,"exp":expire}
    token = jwt.encode(payload,SECRET_KEY,algorithm="HS256")
    return token

def decode_token(token:str) -> str:
    payload = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
    return payload