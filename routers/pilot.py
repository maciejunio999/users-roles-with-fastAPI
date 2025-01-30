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