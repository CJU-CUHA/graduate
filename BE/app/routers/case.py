from fastapi import Depends, HTTPException,status,APIRouter,Header,Request
from sqlalchemy.ext.asyncio import AsyncSession
from model import crud, schemas, database
from typing import List
from fastapi.responses import JSONResponse
import json
import os
from security.jwt import token_func,token_schemas
import jwt
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
        if result:
            return result
        else:
            return JSONResponse(
            content={"message":"Authentication Error"},
            status_code=403
        )
    except Exception as e:
        return JSONResponse(
            content={"message":"Authentication Error"},
            status_code=403
        )



@router.post("")
async def read_Users(Case:schemas.CaseCreate ,db: AsyncSession = Depends(database.get_db),
                     token: HTTPAuthorizationCredentials = Depends(http_bearer)):
    result=await get_User_by_token(db=db,token=token)
    try:
        if isinstance(result, JSONResponse):  # ✅ result가 JSONResponse인지 확인
            return JSONResponse(
                content={"message": "Authentication Fault"},
                status_code=403  # ✅ 인증 실패 시 403 사용
            )

        # ✅ 인증 성공한 경우 Case 생성
        await crud.create_Case(db=db, Case=Case)  # ✅ 비동기 함수이므로 await 추가
        return JSONResponse(
            content={"message": "Creating Case Successful"},
            status_code=200
        )
    except Exception:
        return JSONResponse(
            content={"message": "Error in Creating Case"},
            status_code=400
        )

# 항목 목록 조회
@router.get("", response_model=List[schemas.FindCase])  # 응답 모델 지정
async def list_cases(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db),
                     token: HTTPAuthorizationCredentials = Depends(http_bearer)):
    result = await get_User_by_token(db=db, token=token)
    if isinstance(result, JSONResponse):  # 인증 실패 처리
        raise HTTPException(status_code=403, detail="Authentication Error")

    cases = await crud.get_Cases(db=db, skip=skip, limit=limit)
    
    # models.Case 리스트를 schemas.FindCase 리스트로 변환
    return [
        schemas.FindCase(
            case_id=case.id,
            case_name=case.case_name,
            case_info=case.case_info,
            case_type=case.case_type,
            case_owner=case.case_owner.username if case.case_owner else "Unknown",  # 소유자 이름 반환
            created_at=case.created_at
        )
        for case in cases
    ]

# 항목 수정
@router.put("/{case_id}", response_model=schemas.User)
async def update_case(case_id: int, Case: schemas.CaseCreate, db: AsyncSession = Depends(database.get_db), token: HTTPAuthorizationCredentials = Depends(http_bearer)):
    result = await get_User_by_token(db=db, token=token)
    if isinstance(result, JSONResponse):  # 인증 실패 처리
        raise HTTPException(status_code=403, detail="Authentication Error")

    db_Case = await crud.update_Case(db=db, Case_id=case_id, Case=Case)
    
    if db_Case is None:
        raise HTTPException(status_code=404, detail="Case not found")

    return JSONResponse(content={"message": "Update Successful"}, status_code=status.HTTP_200_OK)


# 항목 삭제
@router.delete("/{case_id}", response_model=schemas.User)
async def delete_case(case_id: int, db: AsyncSession = Depends(database.get_db), token: HTTPAuthorizationCredentials = Depends(http_bearer)):
    result = await get_User_by_token(db=db, token=token)
    if isinstance(result, JSONResponse):  # 인증 실패 처리
        raise HTTPException(status_code=403, detail="Authentication Error")

    db_Case = await crud.delete_Case(db=db, Case_id=case_id)
    
    if db_Case is None:
        raise HTTPException(status_code=404, detail="Case not found")

    return JSONResponse(content={"message": "Delete Successful"}, status_code=status.HTTP_200_OK)