from fastapi import FastAPI, Depends, UploadFile,File,status,APIRouter
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from model import crud, models, schemas, database
from typing import List
from fastapi.responses import JSONResponse
import os
import datetime
import secrets
import json
import jwt
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR,'static/')
IMG_DIR = os.path.join(STATIC_DIR,'images/')
SERVER_IMG_DIR = os.path.join('http://localhost:8000/','static/','images/')
f=open(os.path.join(BASE_DIR,"key.json"),"r")
jwt_password=json.load(f)['jwt_key']

router = APIRouter(
	prefix="/api/proc",
    tags=["proc"]
)
http_bearer = HTTPBearer()

async def get_User_by_token(db: AsyncSession = Depends(database.get_db),token:HTTPAuthorizationCredentials = Depends(http_bearer)):
    bearer_token = token.credentials#왜인지 "이게 맨 처음에 있음.
    try:
        tmp=jwt.decode(jwt=bearer_token,algorithms=["HS256"],key=jwt_password)
    
        email=tmp.get("email")
    
        result=await crud.exist_user(db=db,email=email)
        return result
    except Exception as e:
        return JSONResponse(
            content={"message":"Authentication Error"},
            status_code=403
        )
@router.get("/{case_id}")
async def index(case_id: int):
    return None