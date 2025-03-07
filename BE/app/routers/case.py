from fastapi import Depends, HTTPException,status,APIRouter,Header,Request
from sqlalchemy.ext.asyncio import AsyncSession
from model import crud, schemas, database
import httpx
from fastapi.responses import JSONResponse
import json,jwt
import os
from security.jwt import token_func
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
router = APIRouter(
	prefix="/api/case",
    tags=["case"]
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
f=open(os.path.join(BASE_DIR,"key.json"),"r")
jwt_password=json.load(f)['jwt_key']
# case생성    
http_bearer=HTTPBearer()
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



@router.post("/create")
async def read_Users(Case:schemas.CaseCreate ,db: AsyncSession = Depends(database.get_db),token: HTTPAuthorizationCredentials = Depends(http_bearer)):
    result=get_User_by_token(db=db,token=token)
    try:
        if result:
            crud.create_Case(db=db,Case=Case)
            return JSONResponse(
                content={"message":"Creating Case Successful"},
                status_code=200
            )
        else:
            JSONResponse(
                content={"message":"Authenticatioin Fault"},
                status_code=200
            )
    except Exception as e:
        return JSONResponse(
            content={"message":"Error in Creating Case"},
            status_code=400
        )

# 항목 목록 조회
@router.get("/list")
async def list_cases(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db), token: HTTPAuthorizationCredentials = Depends(http_bearer)):
    result = await get_User_by_token(db=db, token=token)
    if result:
        return await crud.get_Cases(db=db, skip=skip, limit=limit)
    else:
        raise HTTPException(status_code=403, detail="Authentication Error")

# 항목 수정
@router.put("/list/{case_id}", response_model=schemas.User)
async def update_case(case_id: int, Case: schemas.CaseCreate, db: AsyncSession = Depends(database.get_db), token: HTTPAuthorizationCredentials = Depends(http_bearer)):
    result = await get_User_by_token(db=db, token=token)
    if result:
        db_Case = await crud.update_Case(db=db, Case_id=case_id, Case=Case)
        if db_Case is None:
            raise HTTPException(status_code=404, detail="Case not found")
        return JSONResponse(content={"message": "Update Successful"}, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=403, detail="Authentication Error")

# 항목 삭제
@router.delete("/list/{case_id}", response_model=schemas.User)
async def delete_case(case_id: int, db: AsyncSession = Depends(database.get_db), token: HTTPAuthorizationCredentials = Depends(http_bearer)):
    result = await get_User_by_token(db=db, token=token)
    if result:
        db_Case = await crud.delete_Case(db=db, Case_id=case_id)
        if db_Case is None:
            raise HTTPException(status_code=404, detail="Case not found")
        return JSONResponse(content={"message": "Delete Successful"}, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=403, detail="Authentication Error")