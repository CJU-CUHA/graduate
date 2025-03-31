from fastapi import FastAPI, Depends,HTTPException,APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from model import crud, schemas, database
import os
import json
from security.jwt import token_func,token_schemas


router = APIRouter(
	prefix="/api/user",
    tags=["users"]
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

f=open(os.path.join(BASE_DIR,"key.json"),"r")
jwt_password=json.load(f)['jwt_key']
# 회원가입
@router.post("/join", response_model=schemas.Message)
async def create_User(User: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)):
    User.password=token_func.get_password_hash(User.password)
    response = await crud.create_User(db=db, User=User)
    return {"message":response}

# 로그인
@router.post("/login")
async def login_User(User: schemas.User ,db: AsyncSession = Depends(database.get_db)):
    db_User = await crud.user_login(db=db, User=User)
    if db_User is None:
        raise HTTPException(status_code=404, detail="User not found")
    data = {"email": str(db_User.email)}
    access_token = token_func.create_access_token(data=data)
    
    return {
        "access_token": access_token
        }