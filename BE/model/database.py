from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import json
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
f=open(os.path.join(BASE_DIR,"key.json"),"r")
db_password=json.load(f)
DATABASE_URL = f"mysql+aiomysql://root:{db_password['db_password']}@localhost:3306/graduate_security"
 # 예시로 SQLite 사용

# 비동기 엔진 생성
engine = create_async_engine(DATABASE_URL, echo=True)

# 비동기 세션 팩토리
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 의존성: DB 세션을 반환하는 함수
async def get_db():
    async with async_session() as session:
        yield session