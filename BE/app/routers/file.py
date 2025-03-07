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
	prefix="/api/file",
    tags=["file"]
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

# 파일 업로드
@router.post("/upload")
async def file_upload(files: List[UploadFile] = File(), db: AsyncSession = Depends(database.get_db), token: HTTPAuthorizationCredentials = Depends(http_bearer)):
    result = await get_User_by_token(db=db, token=token)
    if result:
        try:
            file_urls = []
            for file in files:
                currentTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                saved_file_name = ''.join([currentTime, secrets.token_hex(16)])
                file_extension = os.path.splitext(file.filename)[1]
                file_location = os.path.join(IMG_DIR, saved_file_name + file_extension)
                
                # 파일 저장
                with open(file_location, "wb+") as file_object:
                    file_object.write(file.file.read())
                    file_urls.append(SERVER_IMG_DIR + saved_file_name)
                
                # 파일 정보 생성
                file_json = {
                    "pc:name": "asdf",  # 여기 필요한 데이터로 수정하세요
                    "file_path": file_urls
                }
                crud.create_File(File=file_json, db=db)
            
            return JSONResponse(
                content={"message": "Request was successful"},
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            return JSONResponse(
                content={"message": "Error", "error": str(e)},
                status_code=status.HTTP_400_BAD_REQUEST
            )
    else:
        return JSONResponse(
            content={"message": "Authentication Error"},
            status_code=status.HTTP_403_FORBIDDEN
        )