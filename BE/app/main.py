from fastapi import FastAPI, Depends, UploadFile,File,HTTPException,status,Response,Security
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi.responses import JSONResponse
from model import crud, models, schemas, database
import os
import datetime
import secrets
import json
from security.jwt import jwtService,jwtEncoder,jwtDecoder
from routers import user,case,file
from security import http_bearer
from fastapi.security import APIKeyHeader

def verify_jwt(access_token=Security(APIKeyHeader(name='access-token'))):
    return access_token

app = FastAPI()
app.include_router(user.router)
app.include_router(case.router)
app.include_router(file.router)

# ✅ 보호된 엔드포인트 (Swagger에서 JWT 토큰 입력 가능)
@app.get("", dependencies=[verify_jwt()], tags=["Authentication"])
async def protected_route():
    return {"message": "You have access to this route"}