from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import schemas, database
from typing import List
from repository import menu
import oauth2


router = APIRouter(
    prefix = '/menu',
    tags = ['Menu']
)

############################################################################################################################################################################################
# BASIC

@router.get('/{user_id}', response_model=List[schemas.ModulePilot])
def get_menu(user_id: int, db: Session = Depends(database.get_db)):
    return menu.get_menu(db, user_id)
