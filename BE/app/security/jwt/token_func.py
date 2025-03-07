from datetime import datetime, timedelta, timezone
from typing import Annotated
import json,os,jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from model import crud
from . import token_schemas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__package__)))
f=open(os.path.join(BASE_DIR,"app\\key.json"),"r")
jwt_password=json.load(f)['jwt_key']

ALGORITHM = "HS256"
ACCEESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"])

oauth2_scheme = HTTPBearer()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authentication_user(username: str, password: str):
    user = crud.get_User(username)
    if not user: 
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict,expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc)+expires_delta
    else:
        expire = datetime.now(timezone.utc)+timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,jwt_password,algorithm=ALGORITHM)
    return encoded_jwt

async def get_cucrrent_user(token:Annotated[str,Depends(oauth2_scheme)]):
    credentials_exception =HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,jwt_password,algorithms=[ALGORITHM])
        username = payload.get("email")
        print(1)
        if username is None:
            raise credentials_exception
        token_data = token_schemas.TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = crud.get_User(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


