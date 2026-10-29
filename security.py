from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()

def hashed_password(password:str) -> str:
    return password_hash.hash((password))

def verify_password(password:str, hashed_pwd:str) -> bool:
    return password_hash.verify(password,hashed_pwd)