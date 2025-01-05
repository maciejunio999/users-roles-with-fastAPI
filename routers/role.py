from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import schemas, database
from typing import List
from repository import role
import oauth2


router = APIRouter(
    prefix = '/role',
    tags = ['Roles']
)

@router.get('/', response_model=List[schemas.CreateRole])
def get_roles(db: Session = Depends(database.get_db)):
    return role.get_all(db)

@router.get('/{id}', response_model=schemas.ShowRole)
def get_role(id: int, db: Session = Depends(database.get_db)):
    return role.get_one(db, id)

@router.post('/', response_model=schemas.CreateRole)
def create_role(request: schemas.CreateRole, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return role.create(request, db)

@router.put('/{id}/add_user', response_model=schemas.ShowRole, status_code=status.HTTP_202_ACCEPTED)
def add_user_to_role(id: int, request: schemas.AddUserToRole, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return role.add_user_to_role(db, id, request)