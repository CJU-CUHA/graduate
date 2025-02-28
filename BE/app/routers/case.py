from fastapi import FastAPI, Depends, HTTPException,status,APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from model import crud, schemas, database

from fastapi.responses import JSONResponse

router = APIRouter(
	prefix="/api/case",
    tags=["case"]
)

# case생성    
@router.post("/create")
async def read_Users( Case:schemas.CaseCreate,db: AsyncSession = Depends(database.get_db)):
    try:

        db_result=await crud.create_Case(Case=Case,db=db)
        print(db_result)
        return JSONResponse(
            content={"message":"Creating case Successful"},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
            content={"message":"Error In Creating case"},
            status_code=status.HTTP_400_BAD_REQUEST
        )


# 항목 목록 조회
@router.get("/list")
async def read_Users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db)):
    return await crud.get_Cases(db=db, skip=skip, limit=limit)

# 항목 수정
@router.put("/list/{case_id}", response_model=schemas.User)
async def update_Case(case_id: int, Case: schemas.CaseCreate, db: AsyncSession = Depends(database.get_db)):
    db_User = await crud.update_Case(db=db, Case_id=case_id, Case=Case)
    if db_User is None:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(
            content={"message":"Update Successful"},
            status_code=status.HTTP_200_OK
        )

# 항목 삭제
@router.delete("/list/{case_id}", response_model=schemas.User)
async def delete_User(case_id: int, db: AsyncSession = Depends(database.get_db)):
    db_User = await crud.delete_Case(db=db, Case_id=case_id)
    if db_User is None:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(
            content={"message":"Delete Successful"},
            status_code=status.HTTP_200_OK
        )