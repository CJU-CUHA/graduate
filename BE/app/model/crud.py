from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from model import models, schemas
from sqlalchemy.sql import and_
from sqlalchemy import JSON
# 항목 생성
async def create_User(db: AsyncSession, User: schemas.UserCreate):
    db_User = models.User(username=User.username,email=User.email,password=User.password)
    if (await db.execute(select(models.User).filter(
        and_(models.User.email == User.email,models.User.username== User.username)))):
        return "existed user"
    else:
        db.add(db_User)
        await db.commit()  # 커밋
        await db.refresh(db_User)  # 객체 새로고침
        return "sign up succesfull"

# 모든 항목 조회
async def get_Users(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.User).offset(skip).limit(limit))
    return result.scalars().all()

# 특정 항목 조회
async def get_User(db: AsyncSession, User_username):
    result = await db.execute(select(models.User).filter(models.User.username == User_username))
    return result.scalars().first()

# 로그인
async def user_login(db: AsyncSession, User ):
    result = await db.execute(select(models.User).filter(
        and_(
            models.User.email == User.email,
            models.User.password == User.password
        )))
    return result.scalars().first()

# 항목 업데이트
async def update_User(db: AsyncSession, User_id: int, User: schemas.UserCreate):
    db_User = await get_User(db, User_id)
    if db_User:
        db_User.username = User.name
        db_User.email = User.email
        db_User.password = User.password
        await db.commit()
        await db.refresh(db_User)
    return db_User

# 항목 삭제
async def delete_User(db: AsyncSession, User_id: int):
    db_User = await get_User(db, User_id)
    if db_User:
        await db.delete(db_User)
        await db.commit()
    return db_User

# 항목 생성
async def create_File(db: AsyncSession, File: schemas.CreateFile):
    db_User = models.File(pc_name=File.pc_name,file_path=File.file_path)
    db.add(db_User)
    await db.commit()  # 커밋
    await db.refresh(db_User)  # 객체 새로고침
    return db_User

# 모든 항목 조회
async def get_Files(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.File).offset(skip).limit(limit))
    return result.scalars().all()

# 특정 항목 조회
async def get_File(db: AsyncSession, File_id: int):
    result = await db.execute(select(models.File).filter(models.File.id == File_id))
    return result.scalars().first()

# 항목 업데이트
async def update_File(db: AsyncSession, File_id: int, File: schemas.CreateFile):
    db_File = await get_File(db, File_id)
    if db_File:
        db_File.pc_name = File.pc_name
        db_File.files = File.files
        db_File._case = File._case
        await db.commit()
        await db.refresh(db_File)
    return db_File

# 항목 삭제
async def delete_Delete(db: AsyncSession, File_id: int):
    db_File = await get_File(db, File_id)
    if db_File:
        await db.delete(db_File)
        await db.commit()
    return db_File

# 항목 생성
async def create_Case(db: AsyncSession, Case: schemas.CaseCreate):
    db_Case = models.Case(case_name=Case.case_name,case_info=Case.case_info, case_type=Case.case_type, case_owner=Case.case_owner)
    db.add(db_Case)
    await db.commit()  # 커밋
    await db.refresh(db_Case)  # 객체 새로고침
    # 세션 닫기
    await db.close()
    return db_Case

# 모든 항목 조회
async def get_Cases(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.Case).offset(skip).limit(limit))
    return result.scalars().all()

# 특정 항목 조회
async def get_Case(db: AsyncSession, Case_id: int):
    result = await db.execute(select(models.Case).filter(models.Case.id == Case_id))
    return result.scalars().first()

# 항목 업데이트
async def update_Case(db: AsyncSession, Case_id: int, Case: schemas.CaseCreate):
    db_Case = await get_Case(db, Case_id)
    if db_Case:
        db_Case.case_name = Case.case_name
        db_Case.case_info= Case.case_info
        db_Case.case_type = Case.case_type
        db_Case.case_owner = Case.case_owner
        await db.commit()
        await db.refresh(db_Case)
    return db_Case

# 항목 삭제
async def delete_Case(db: AsyncSession, Case_id: int):
    db_Case = await get_Case(db, Case_id)
    if db_Case:
        await db.delete(db_Case)
        await db.commit()
    return db_Case


async def exist_user(db: AsyncSession, email: str):
    # 사용자가 존재하는지 확인하는 쿼리
    stmt = select(models.User).filter(models.User.email == email)
    result = await db.execute(stmt)
    # 결과에서 첫 번째 항목을 가져옴 (사용자가 있으면 첫 번째 사용자 반환)
    return result.scalars().first()

async def create_Case(db: AsyncSession, Case: schemas.CaseCreate):
    db_Case = models.Case(case_name=Case.case_name,case_info=Case.case_info, case_type=Case.case_type, case_owner=Case.case_owner)
    db.add(db_Case)
    await db.commit()  # 커밋
    await db.refresh(db_Case)  # 객체 새로고침
    # 세션 닫기
    await db.close()
    return db_Case