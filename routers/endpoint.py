from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import schemas, database
from typing import List
from repository import endpoint
import oauth2
from access import require_roles


router = APIRouter(
    prefix = '/endpoint',
    tags = ['Endpoint']
)


############################################################################################################################################################################################
# BASIC

@router.get('/', response_model=List[schemas.ShowEndpoint])
def get_endpoints(db: Session = Depends(database.get_db)):
    return endpoint.get_all(db)


@router.get('/{id}', response_model=schemas.ShowFullEndpoint)
def get_endpoint(id: int, db: Session = Depends(database.get_db)):
    return endpoint.get_one(db, id)


@router.post('/', response_model=schemas.ShowEndpoint)
def create_endpoint(request: schemas.CreateEndpoint, db: Session = Depends(database.get_db)):
    return endpoint.create(request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_endpoint(id: int, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return endpoint.delete(db, id)


@router.put('/{id}', response_model=schemas.ShowEndpoint, status_code=status.HTTP_202_ACCEPTED)
def update_endpoint(id: int, request: schemas.CreateEndpoint, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return endpoint.update(db, id, request)

############################################################################################################################################################################################
# ROLES

@router.get('/{id}/roles', response_model=schemas.EndpointRoles)
def get_pilots_roles(id: int, db: Session = Depends(database.get_db)):
    return endpoint.get_endpoint_roles(db, id)


@router.put('/{id}/add_role', response_model=schemas.EndpointRoles, status_code=status.HTTP_202_ACCEPTED)
def add_role_to_pilot(id: int, request: schemas.AddById, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return endpoint.add_role_to_endpoint(db, id, request)


@router.delete("/{id}/remove_role", status_code=status.HTTP_204_NO_CONTENT)
def remove_role_from_pilot(id: int, request: schemas.AddById, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return endpoint.remove_role_from_endpoint(db=db, id=id, request=request)