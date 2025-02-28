from fastapi import FastAPI, Depends, UploadFile,File,status,APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from model import crud, models, schemas, database
from typing import List
from fastapi.responses import JSONResponse
import os
import datetime
import secrets


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BE_DIR= os.path.join(BASE_DIR,'BE/')
STATIC_DIR = os.path.join(BE_DIR,'static/')
IMG_DIR = os.path.join(STATIC_DIR,'images/')
SERVER_IMG_DIR = os.path.join('http://localhost:8000/','static/','images/')


router = APIRouter(
	prefix="/api/file",
    tags=["file"]
)
@router.post("/upload")
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
    