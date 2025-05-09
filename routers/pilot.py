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
def create_pilot(request: schemas.CreatePilot, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return pilot.create(request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_pilot(id: int, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return pilot.delete(db, id)


@router.put('/{id}', response_model=schemas.ShowPilot, status_code=status.HTTP_202_ACCEPTED)
def update_pilot(id: int, request: schemas.CreatePilot, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return pilot.update_pilot(db, id, request)


############################################################################################################################################################################################
# ACTIVATION

@router.put('/activate/{id}', response_model=schemas.ShowPilot, status_code=status.HTTP_202_ACCEPTED)
def activate_pilot(id: int, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return pilot.activate_pilot(db, id)

@router.put('/deactivate/{id}', response_model=schemas.ShowPilot, status_code=status.HTTP_202_ACCEPTED)
def deactivate_pilot(id: int, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return pilot.deactivate_pilot(db, id)


############################################################################################################################################################################################
# ROLES

@router.get('/{id}/roles', response_model=schemas.PilotRoles)
def get_pilots_roles(id: int, db: Session = Depends(database.get_db)):
    return pilot.get_pilots_roles(db, id)


@router.put('/{id}/add_role', response_model=schemas.PilotRoles, status_code=status.HTTP_202_ACCEPTED)
def add_role_to_pilot(id: int, request: schemas.AddById, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return pilot.add_role_to_pilot(db, id, request)


@router.delete("/{id}/remove_role", status_code=status.HTTP_204_NO_CONTENT)
def remove_role_from_pilot(id: int, request: schemas.AddById, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return pilot.remove_role_from_pilot(db=db, id=id, request=request)


############################################################################################################################################################################################
# USERS

@router.get('/{id}/users', response_model=schemas.PilotUsers)
def get_pilots_users(id: int, db: Session = Depends(database.get_db)):
    return pilot.get_pilots_users(db, id)


@router.put('/{id}/add_user', response_model=schemas.PilotUsers, status_code=status.HTTP_202_ACCEPTED)
def add_user_to_pilot(id: int, request: schemas.AddById, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return pilot.add_user_to_pilot(db, id, request)


@router.delete("/{id}/remove_user", status_code=status.HTTP_204_NO_CONTENT)
def remove_user_from_pilot(id: int, request: schemas.AddById, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return pilot.remove_user_from_pilot(db=db, id=id, request=request)