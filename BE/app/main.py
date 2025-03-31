from fastapi import FastAPI, Depends, UploadFile,File,HTTPException,status,Response,Security,Header

from routers import user,case,file,mapping,proc
from fastapi.security import APIKeyHeader

from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBearer

from model import crud
from security.jwt import token_func,token_schemas

ACCESS_TOKEN_EXPIRE_MINUTES = 30
app = FastAPI()
app.include_router(user.router)
app.include_router(case.router)
app.include_router(file.router)
app.include_router(proc.router)
app.include_router(mapping.router)
# ✅ 보호된 엔드포인트 (Swagger에서 JWT 토큰 입력 가능)
http_bearer=HTTPBearer()
@app.get("/items/")
async def read_items(token: Annotated[str, Depends(http_bearer)]):
    return {"Authorization":f"Bearer {token}"}

# @app.post("/token")
# async def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
# ) -> token_schemas.Token:
#     user = token_func.authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = token_func.create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return token_schemas.Token(access_token=access_token, token_type="bearer")