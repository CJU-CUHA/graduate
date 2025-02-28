from fastapi import FastAPI, Depends,HTTPException,APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from model import crud, schemas, database
import os
import json
from security.jwt import jwtService,jwtEncoder,jwtDecoder


router = APIRouter(
	prefix="/api/user",
    tags=["users"]
)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


f=open(os.path.join(BASE_DIR,"key.json"),"r")
jwt_password=json.load(f)['jwt_key']
jwt_service = jwtService.JWTService(jwtEncoder.JWTEncoder(), jwtDecoder.JWTDecoder(),secret_key=jwt_password,
    algorithm="HS256",  # ✅ None이 아니라 올바른 알고리즘 사용
    access_token_expire_time=30)  # 30분 유효기간)
# 회원가입
@router.post("/join", response_model=schemas.User)
async def create_User(User: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.create_User(db=db, User=User)

# 로그인
@router.post("/login")
async def login_User(User: schemas.User ,db: AsyncSession = Depends(database.get_db)):
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