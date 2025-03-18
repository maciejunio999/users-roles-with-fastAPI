from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import schemas, database
from typing import List
from repository import module
import oauth2


router = APIRouter(
    prefix = '/module',
    tags = ['Modules']
)

############################################################################################################################################################################################
# BASIC

@router.get('/', response_model=List[schemas.Module])
def get_modules(db: Session = Depends(database.get_db)):
    return module.get_all(db)


@router.get('/{id}', response_model=schemas.ShowFullModule)
def get_module(id: int, db: Session = Depends(database.get_db)):
    return module.get_one(db, id)


@router.post('/', response_model=schemas.Module)
def create_module(request: schemas.CreateModule, db: Session = Depends(database.get_db)):
    return module.create(request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_module(id: int, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return module.delete(db, id)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_module(id: int, request: schemas.CreateModule, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return module.update(db, id, request)