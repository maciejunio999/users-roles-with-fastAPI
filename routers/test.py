from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import schemas, database
from typing import List
#from repository import 
import oauth2
from access import require_roles


router = APIRouter(
    prefix = '/test',
    tags = ['Test']
)


############################################################################################################################################################################################
# BASIC

@router.get('/')
def get(current_user=Depends(require_roles("R1"))):
    return {'Test': 'test'}