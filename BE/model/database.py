from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import databases
import json
with open("model\\key.json", 'r') as f:
    db_password = json.load(f)
# MySQL 연결 정보 (본인 설정에 맞게 변경)
DATABASE_URL = f"mysql+aiomysql://root:{db_password['db_password']}@localhost:3306/graduate_security"
# 비동기 엔진 생성
engine = create_async_engine(DATABASE_URL, echo=True)

# 세션 팩토리 생성
async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# FastAPI databases 사용 (선택사항)
database = databases.Database(DATABASE_URL)

# Dependency: DB 세션 생성
async def get_db():
    async with async_session() as session:
        yield session
