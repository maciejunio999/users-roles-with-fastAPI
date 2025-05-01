from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import schemas, database
from typing import List
from repository import product
import oauth2
import access

router = APIRouter(
    prefix = '/product',
    tags = ['Product']
)


CONFIGURATION = {
    'get_all': 'AD',
    'get_one': 'R1',
    'create': 'AD',
    'update': 'AD',
    'delete': 'AD',
    'activation': 'AD'
}


############################################################################################################################################################################################
# BASIC

@router.get('/', response_model=List[schemas.CreateProduct])
def get_products(db: Session = Depends(database.get_db), require_roles: schemas.User = Depends(access.require_any_role(CONFIGURATION['get_all'], CONFIGURATION['get_one']))):
    return product.get_all(db)


@router.get('/{id}', response_model=schemas.ShowProduct)
def get_product(id: int, db: Session = Depends(database.get_db), require_roles: schemas.User = Depends(access.require_any_role(CONFIGURATION['get_all'], CONFIGURATION['get_one']))):
    return product.get_one(db, id)


@router.post('/', response_model=schemas.CreateProduct)
def create_product(request: schemas.CreateProduct, db: Session = Depends(database.get_db), require_roles: schemas.User = Depends(access.require_roles(CONFIGURATION['create'])), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return product.create(request, db)


@router.put('/{id}', response_model=schemas.ShowProduct, status_code=status.HTTP_202_ACCEPTED)
def update_product(id: int, request: schemas.CreateProduct, db: Session = Depends(database.get_db), require_roles: schemas.User = Depends(access.require_roles(CONFIGURATION['update'])), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return product.update_product(db, id, request)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(database.get_db), require_roles: schemas.User = Depends(access.require_roles(CONFIGURATION['delete'])), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return product.delete(db, id)


############################################################################################################################################################################################
# ACTIVATION

@router.put('/activate/{id}', response_model=schemas.ShowProduct, status_code=status.HTTP_202_ACCEPTED)
def activate_product(id: int, db: Session = Depends(database.get_db), require_roles: schemas.User = Depends(access.require_roles(CONFIGURATION['activation'])), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return product.activate_product(db, id)

@router.put('/deactivate/{id}', response_model=schemas.ShowProduct, status_code=status.HTTP_202_ACCEPTED)
def deactivate_product(id: int, db: Session = Depends(database.get_db), require_roles: schemas.User = Depends(access.require_roles(CONFIGURATION['activation'])), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return product.deactivate_product(db, id)

