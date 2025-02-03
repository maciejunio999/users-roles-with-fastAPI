from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import schemas, database
from typing import List
from repository import pilot
import oauth2


router = APIRouter(
    prefix = '/pilot',
    tags = ['Pilots']
)

############################################################################################################################################################################################
# BASIC

@router.get('/', response_model=List[schemas.ShowPilot])
def get_pilots(db: Session = Depends(database.get_db)):
    return pilot.get_all(db)


@router.get('/{id}', response_model=schemas.ShowFullPilot)
def get_pilot(id: int, db: Session = Depends(database.get_db)):
    return pilot.get_one(db, id)


@router.post('/', response_model=schemas.ShowPilot)
def create_pilot(request: schemas.ShowPilot, db: Session = Depends(database.get_db)):
    return pilot.create(request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_pilot(id: int, db: Session = Depends(database.get_db)):
    return pilot.delete(db, id)


@router.put('/{id}', response_model=schemas.ShowPilot, status_code=status.HTTP_202_ACCEPTED)
def update_pilot(id: int, request: schemas.ShowPilot, db: Session = Depends(database.get_db)):
    return pilot.update_pilot(db, id, request)

############################################################################################################################################################################################
# ROLES

@router.get('/{id}/roles', response_model=schemas.PilotRoles)
def get_pilots_roles(id: int, db: Session = Depends(database.get_db)):
    return pilot.get_pilots_roles(db, id)


@router.put('/{id}/add_role', response_model=schemas.ShowPilotAndRoles, status_code=status.HTTP_202_ACCEPTED)
def add_role_to_pilot(id: int, request: schemas.AddRoleToPilot, db: Session = Depends(database.get_db)):
    return pilot.add_role_to_pilot(db, id, request)


@router.delete("/{id}/remove_role", response_model=schemas.ShowPilotAndRoles, status_code=status.HTTP_200_OK)
def remove_role_from_pilot(id: int, request: schemas.AddRoleToPilot, db: Session = Depends(database.get_db)):
    return pilot.remove_role_from_pilot(db=db, id=id, request=request)

############################################################################################################################################################################################
# USERS

@router.get('/{id}/users', response_model=schemas.PilotUsers)
def get_pilots_users(id: int, db: Session = Depends(database.get_db)):
    return pilot.get_pilots_users(db, id)


@router.put('/{id}/add_user', response_model=schemas.ShowPilotAndUsers, status_code=status.HTTP_202_ACCEPTED)
def add_user_to_pilot(id: int, request: schemas.AddUserToPilot, db: Session = Depends(database.get_db)):
    return pilot.add_user_to_pilot(db, id, request)


@router.delete("/{id}/remove_user", response_model=schemas.ShowPilotAndUsers, status_code=status.HTTP_200_OK)
def remove_user_from_pilot(id: int, request: schemas.AddUserToPilot, db: Session = Depends(database.get_db)):
    return pilot.remove_user_from_pilot(db=db, id=id, request=request)