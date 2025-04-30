from sqlalchemy.orm import Session, joinedload
import models, schemas
from fastapi import status, HTTPException


############################################################################################################################################################################################
# BASIC

def get_all(db: Session):
    endpoints = db.query(models.Endpoint).all()
    if not endpoints:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is none")
    return endpoints


def get_one(db: Session, id: int):
    endpoint = db.query(models.Endpoint).filter(models.Endpoint.id == id).first()
    if not endpoint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Endpoint with id {id} not found")
    return endpoint


def create(request: schemas.CreateEndpoint, db: Session):
    if len(db.query(models.Endpoint).filter(models.Endpoint.name == request.name).all()) >= 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"This name is already taken")
    
    if len(db.query(models.Endpoint).filter(models.Endpoint.url == request.url).all()) >= 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"This code is already taken")
    
    new_endpoint = models.Endpoint(name=request.name, url=request.url, description=request.description)
    db.add(new_endpoint)
    db.commit()
    db.refresh(new_endpoint)
    return new_endpoint


def delete(db: Session, id: int):
    endpoint_query = db.query(models.Endpoint).filter(models.Endpoint.id == id)
    endpoint = endpoint_query.first()

    if not endpoint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Endpoint with id {id} not found")
    
    endpoint_query.delete(synchronize_session=False)
    db.commit()
    return {'details': 'Endpoint Deleted'}


def update(db: Session, id: int, request: schemas.CreateModule):
    endpoint = db.query(models.Endpoint).filter(models.Endpoint.id == id).first()

    if not endpoint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Endpoint with id {id} not found")
    
    if len(db.query(models.Endpoint).filter(models.Endpoint.name == request.name).all()) >= 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"This name is already taken")
    
    if len(db.query(models.Endpoint).filter(models.Endpoint.url == request.url).all()) >= 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"This code is already taken")
    
    endpoint.name = request.name
    endpoint.description = request.description
    db.commit()
    db.refresh(endpoint)

    return {'details': 'Endpoint Updated'}


############################################################################################################################################################################################
# ROLES

def get_endpoint_roles(db: Session, id: int):
    endpoint = db.query(models.Endpoint).filter(models.Endpoint.id == id).first()

    if not endpoint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Endpoint with id {id} not found")
    
    roles = [schemas.ShowRole.from_orm(r) for r in endpoint.roles]

    return schemas.EndpointRoles(id=endpoint.id, name=endpoint.name, url=endpoint.url, description=endpoint.description, http_method=endpoint.http_method, roles=roles)


def add_role_to_endpoint(db: Session, id: int, request: schemas.AddById):
    endpoint = db.query(models.Endpoint).filter(models.Endpoint.id == id).first()
    role = db.query(models.Role).filter(models.Role.id == request.id).first()
    
    if not (endpoint and role):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Endpoint with id: {id} or Role with id: {request.id} not found")

    if role not in endpoint.roles:
        endpoint.roles.append(role)
        db.commit()
        db.refresh(endpoint)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Endpoint with id: {id} already has Role with id: {request.id}")

    roles = [schemas.ShowRole.from_orm(r) for r in endpoint.roles]

    return schemas.EndpointRoles(id=endpoint.id, name=endpoint.name, url=endpoint.url, description=endpoint.description, http_method=endpoint.http_method, roles=roles)


def remove_role_from_endpoint(db: Session, id: int, request: schemas.AddById):
    endpoint = db.query(models.Endpoint).options(joinedload(models.Endpoint.roles)).filter(models.Endpoint.id == id).first()
    if not endpoint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Endpoint with id: {request.id} not found")
    
    role = db.query(models.Role).filter(models.Role.id == request.id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id: {request.id} not found")
    
    if role not in endpoint.roles:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Endpoint does not have this role assigned")
    
    endpoint.roles.remove(role)
    db.commit()
    db.refresh(endpoint)

    return {'details': 'Role Deleted'}