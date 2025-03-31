from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import JSON
# 유저 생성용 스키마
class UserCreate(BaseModel):
    username: str
    password: str
    email: str

# 유저 조회용 스키마
class User(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True

# 사건 생성용 스키마
class CaseCreate(BaseModel):
    case_name: str
    case_info: str
    case_type: str
    case_owner: str

# 사건 조회용 스키마
class FindCase(BaseModel):  # findCase -> FindCase (클래스명은 보통 대문자로 시작)
    case_id: int
    case_name: str
    case_info: str
    case_type: str
    case_owner: str
    created_at: datetime  # DateTime -> datetime.datetime으로 수정

    class Config:
        from_attributes = True

# 파일 업로드 관련 스키마
class CreateFile(BaseModel):
    pc_name: str
    file_path: str  # 바이너리 저장이 아니라 경로 저장 방식 유지

    class Config:
        from_attributes = True

# 실제 데이터베이스 모델을 위한 `File` 모델
class File(BaseModel):
    id: int
    pc_name: str
    files: bytes  # 파일을 직접 저장하는 경우, 보통 LargeBinary를 사용

    class Config:
        from_attributes = True

# 메시지 응답 스키마
class Message(BaseModel):
    message: str

class Logs(BaseModel):
    alias: str
    channel:str
    event_data:JSON
    computer:str