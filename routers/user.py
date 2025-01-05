from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import schemas, database
from typing import List
from repository import user
import oauth2


router = APIRouter(
    prefix = '/user',
    tags = ['Users']
)


@router.get('/', response_model=List[schemas.ShowUser])
def get_users(db: Session = Depends(database.get_db)):
    return user.get_all(db)


@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.get_one(db, id)


@router.get('/{id}/roles', response_model=schemas.UserRoles)
def get_users_roles(id: int, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.get_users_roles(db, id)


@router.post('/', response_model=schemas.BaseUser)
def create_user(request: schemas.BaseUser, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.create(request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.delete(db, id)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_user(id: int, request: schemas.UpdateUser, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.update(db, id, request)


@router.put('/{id}/add_role', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.UserRoles)
def add_role_to_user(id: int, request: schemas.UpdateUserRole, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.add_role_to_user(db, id, request)