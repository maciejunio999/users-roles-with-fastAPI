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


############################################################################################################################################################################################
# BASIC

@router.get('/', response_model=List[schemas.CreateRole])
def get_roles(db: Session = Depends(database.get_db)):
    return role.get_all(db)


@router.get('/{id}', response_model=schemas.ShowFullRole)
def get_role(id: int, db: Session = Depends(database.get_db)):
    return role.get_one(db, id)


@router.post('/', response_model=schemas.CreateRole)
def create_role(request: schemas.CreateRole, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return role.create(request, db)


@router.put('/{id}', response_model=schemas.ShowFullRole, status_code=status.HTTP_202_ACCEPTED)
def update_role(id: int, request: schemas.CreateRole, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return role.update_role(db, id, request)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_role(id: int, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return role.delete(db, id)


############################################################################################################################################################################################
# USERS

@router.get('/{id}/users', response_model=schemas.RoleUsers)
def get_roles_users(id: int, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return role.get_roles_users(db, id)


@router.put('/{id}/add_user', response_model=schemas.ShowFullRole, status_code=status.HTTP_202_ACCEPTED)
def add_user_to_role(id: int, request: schemas.AddById, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return role.add_user_to_role(db, id, request)


@router.delete("/{id}/remove_user", status_code=status.HTTP_204_NO_CONTENT)
def remove_role_from_user(id: int, request: schemas.AddById, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return role.remove_user_from_role(db=db, id=id, request=request)


############################################################################################################################################################################################
# PILOTS

@router.get('/{id}/pilots', response_model=schemas.RolePilots)
def get_roles_pilots(id: int, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return role.get_roles_pilots(db, id)


@router.put('/{id}/add_pilot', response_model=schemas.ShowFullRole, status_code=status.HTTP_202_ACCEPTED)
def add_pilot_to_role(id: int, request: schemas.AddById, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return role.add_pilot_to_role(db, id, request)


@router.delete('/{id}/remove_pilot', status_code=status.HTTP_204_NO_CONTENT)
def remove_pilot_from_role(id: int, request: schemas.AddById, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return role.remove_pilot_from_role(db=db, id=id, request=request)
