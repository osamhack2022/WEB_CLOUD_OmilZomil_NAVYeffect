from typing import List
from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.crud import vacation as crud
from app.schemas.user import UserReadResponse
from app.schemas import vacation as schema
from app.api import deps


router = APIRouter()


@router.post("/{user_id}", response_model=schema.VacationResponse)
async def create_vacation(user_id: int, vacation: schema.VacationCreate = Body(), db: Session = Depends(deps.get_db)):
    return crud.create_vacation(db, user_id, vacation)


@router.get("/{user_id}", response_model=List[schema.VacationRead])
def get_vacations(user_id: int, db: Session = Depends(deps.get_db)):
    return crud.get_vacations(db, user_id=user_id)


@router.get("/", response_model=List[schema.VacationRead])
def get_vacations_from_unit(user_id: int, db: Session = Depends(deps.get_db), current_user: UserReadResponse = Depends(deps.get_current_user)):
    return crud.get_vacations(db, unit_id=current_user.military_unit)


@router.put("/approval/{vacation_id}", response_model=schema.VacationResponse)
async def update_vacation_approval(user_id: int, vacation_id: int, is_approved: schema.VacationUpdateApproval = Body(), db: Session = Depends(deps.get_db)):
    return crud.update_vacation_approval(db, vacation_id, is_approved)


@router.delete("/{user_id}/{vacation_id}", response_model=schema.VacationResponse)
def delete_vacation(user_id: int, vacation_id: int, db: Session = Depends(deps.get_db)):
    return crud.delete_vacation(db, vacation_id)