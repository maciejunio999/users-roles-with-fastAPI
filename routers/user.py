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


############################################################################################################################################################################################
# BASIC

@router.get('/', response_model=List[schemas.ShowUser])
def get_users(db: Session = Depends(database.get_db)):
    return user.get_all(db)

@router.get('/{id}', response_model=schemas.ShowFullUser)
def get_user(id: int, db: Session = Depends(database.get_db)):
    return user.get_one(db, id)

@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    return user.create(request, db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.delete(db, id)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_user(id: int, request: schemas.User, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.update(db, id, request)


############################################################################################################################################################################################
# ROLES

@router.get('/{id}/roles', response_model=schemas.UserRoles)
def get_users_roles(id: int, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.get_users_roles(db, id)

@router.put('/{id}/add_role', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.UserRoles)
def add_role_to_user(id: int, request: schemas.AddById, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.add_role_to_user(db, id, request)

@router.delete("/{id}/remove_role", status_code=status.HTTP_204_NO_CONTENT)
def remove_role_from_user(id: int, request: schemas.AddById, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.remove_role_from_user(db=db, id=id, request=request)


############################################################################################################################################################################################
# PILOTS

@router.get('/{id}/pilots', response_model=schemas.UserPilots)
def get_users_pilots(id: int, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.get_users_pilots(db, id)


@router.get('/{id}/active_pilots', response_model=schemas.UserPilots)
def get_users_active_pilots(id: int, db: Session = Depends(database.get_db)):
    return user.get_users_active_pilots(db, id)


@router.put('/{id}/add_pilot', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.UserPilots)
def add_pilot_to_user(id: int, request: schemas.AddById, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.add_pilot_to_user(db, id, request)


@router.delete("/{id}/remove_pilot", status_code=status.HTTP_204_NO_CONTENT)
def remove_pilot_from_user(id: int, request: schemas.AddById, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.remove_pilot_from_user(db=db, id=id, request=request)