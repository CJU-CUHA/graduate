from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, func, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
import datetime

# Create and Update 스키마 (유저 생성용)
class UserCreate(BaseModel):
    username: str
    password: str
    email: str
# 응답 스키마 (유저 조회용)
class User(BaseModel):
    email: str
    password: str
    
    class Config:
        from_attributes = True

# Create와 Update 스키마 (사건 생성용)
class CaseCreate(BaseModel):
    case_name: str
    case_info: str
    case_type: str
    case_owner: str

# 응답 스키마 (사건 조회용)
class Case(BaseModel):
    case_name: str
    case_info: str
    case_type: str
    case_owner: str

    class Config:
        from_attributes = True  # ORM 모델과 Pydantic 모델 간의 호환성을 위해 필요

# 파일 업로드와 관련된 스키마
class CreateFile(BaseModel):
    pc_name: str
    file_path: str
      # 파일을 바이너리 형태로 저장 (Pydantic에서는 `bytes`로 처리)
    # _case: int  # 외래 키로 사용하는 case ID (필요에 따라 필드명 변경 가능)

    class Config:
        from_attributes = True  # ORM 모델과 Pydantic 모델 간의 호환성을 위해 필요

# 실제 데이터베이스 모델을 위한 `File` 모델
class File(BaseModel):
    id: int
    pc_name: str
    files: bytes  # Pydantic에서 바이너리 데이터는 `bytes`로 처리됨
    # case_id: int  # 외래 키 필드 (사건과 연결)

    class Config:
        from_attributes = True  # ORM 모델과 Pydantic 모델 간의 호환성을 위해 필요

class Message(BaseModel):
    message: str