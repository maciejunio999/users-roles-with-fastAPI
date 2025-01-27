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


@router.get('/', response_model=List[schemas.ShowFullPilot])
def get_pilots(db: Session = Depends(database.get_db)):
    return pilot.get_all(db)


@router.post('/', response_model=schemas.CreatePilot)
def create_pilot(request: schemas.CreatePilot, db: Session = Depends(database.get_db)):
    return pilot.create(request, db)