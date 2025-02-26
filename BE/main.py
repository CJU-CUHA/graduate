from fastapi import FastAPI, Depends, UploadFile,File,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from model import crud, models, schemas, database
from typing import List
from fastapi.responses import JSONResponse
import os
import datetime
import secrets
import json
from security.jwt import jwtService,jwtEncoder,jwtDecoder

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BE_DIR= os.path.join(BASE_DIR,'BE/')
STATIC_DIR = os.path.join(BE_DIR,'static/')
IMG_DIR = os.path.join(STATIC_DIR,'images/')
SERVER_IMG_DIR = os.path.join('http://localhost:8000/','static/','images/')

f=open(os.path.join(BE_DIR,"key.json"),"r")
jwt_password=json.load(f)['jwt_key']
jwt_service = jwtService.JWTService(jwtEncoder.JWTEncoder(), jwtDecoder.JWTDecoder(),secret_key=jwt_password,
    algorithm="HS256",  # ✅ None이 아니라 올바른 알고리즘 사용
    access_token_expire_time=30)  # 30분 유효기간)


# DB 초기화
@app.on_event("startup")
async def startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

# 회원가입
@app.post("/api/user/join", response_model=schemas.User)
async def create_User(User: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.create_User(db=db, User=User)

# 로그인
@app.post("/api/users/login")
async def login_User(User: schemas.User, db: AsyncSession = Depends(database.get_db)):
    db_User = await crud.user_login(db=db, User=User)
    if db_User is None:
        raise HTTPException(status_code=404, detail="User not found")
    data = {"id": str(db_User.id)}
    access_token = jwt_service.create_access_token(data)
    refresh_token = jwt_service.create_refresh_token(data)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
    

#파일 업로드
@app.post("/api/file/upload")
async def file_upload(files: List[UploadFile]= File(),db: AsyncSession = Depends(database.get_db)):
    try:
        file_urls=[]
        for file in files:
            currentTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            saved_file_name = ''.join([currentTime,secrets.token_hex(16)])
            # print(saved_file_name)
            file_extension = os.path.splitext(file.filename)[1]
            file_location = os.path.join(IMG_DIR,saved_file_name+file_extension)
            with open(file_location, "wb+") as file_object:
                file_object.write(file.file.read())
                file_urls.append(SERVER_IMG_DIR+saved_file_name)
                file_json={
                "pc:name":"asdf",
                "file_path":file_urls
                    }
            crud.create_File(File=file_json,db=db)
    # db_File = await crud.create_File(File=,db=db)
        return JSONResponse(
            content={"message": "Request was successful",
                },
            status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(
            content={"message":"Error"},
            status_code=status.HTTP_400_BAD_REQUEST)

# case생성    
@app.post("/api/case/create")
async def read_Users( Case:schemas.CaseCreate,db: AsyncSession = Depends(database.get_db)):
    try:

        db_result=await crud.create_Case(Case=Case,db=db)
        print(db_result)
        return JSONResponse(
            content={"message":"Creating case Successful"},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
            content={"message":"Error In Creating case"},
            status_code=status.HTTP_400_BAD_REQUEST
        )


# 항목 목록 조회
@app.get("/api/case/list/")
async def read_Users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db)):
    return await crud.get_Cases(db=db, skip=skip, limit=limit)

# 항목 수정
@app.put("/api/case/list/{case_id}", response_model=schemas.User)
async def update_Case(case_id: int, Case: schemas.CaseCreate, db: AsyncSession = Depends(database.get_db)):
    db_User = await crud.update_Case(db=db, Case_id=case_id, Case=Case)
    if db_User is None:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(
            content={"message":"Update Successful"},
            status_code=status.HTTP_200_OK
        )

# 항목 삭제
@app.delete("/api/create/list/{case_id}", response_model=schemas.User)
async def delete_User(case_id: int, db: AsyncSession = Depends(database.get_db)):
    db_User = await crud.delete_Case(db=db, Case_id=case_id)
    if db_User is None:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(
            content={"message":"Delete Successful"},
            status_code=status.HTTP_200_OK
        )