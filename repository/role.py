from sqlalchemy.orm import Session, joinedload
import models, schemas
from fastapi import status, HTTPException
from typing import List


############################################################################################################################################################################################
# BASIC

def get_all(db: Session):
    roles = db.query(models.Role).all()
    if not roles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is none")
    return roles


def get_one(db: Session, id: int):
    role = db.query(models.Role).filter(models.Role.id == id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id {id} not found")

    return role


def create(request: schemas.CreateRole, db: Session):
    if len(db.query(models.Role).filter(models.Role.name == request.name).all()) >= 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"This name is already taken")
    
    if len(db.query(models.Role).filter(models.Role.code == request.code).all()) >= 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"This code is already taken")
    
    new_role = models.Role(name=request.name, code=request.code, description=request.description)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role


def update_role(db: Session, id: int, request: schemas.CreateRole):
    role = db.query(models.Role).filter(models.Role.id == id).first()

    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id {id} not found")
    
    if len(db.query(models.Role).filter(models.Role.name == request.name).all()) >= 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"This name is already taken")
    
    if len(db.query(models.Role).filter(models.Role.code == request.code).all()) >= 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"This code is already taken")
    
    role.name = request.name
    role.code = request.code
    role.description = request.description
    db.commit()
    db.refresh(role)

    return schemas.ShowRole(id=role.id, name=role.name, code=role.code, description=role.description)


def delete(db: Session, id: int):
    role_query = db.query(models.Role).filter(models.Role.id == id)
    role = role_query.first()

    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id {id} not found")
    
    role_query.delete(synchronize_session=False)
    db.commit()
    return {'details': 'Role Deleted'}


############################################################################################################################################################################################
# USERS

def get_roles_users(db: Session, id: int):
    role = db.query(models.Role).filter(models.Role.id == id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id {id} not found")
    users = [schemas.ShowUser.from_orm(u) for u in role.users]
    return schemas.RoleUsers(id=role.id, name=role.name, code=role.code, description=role.description, users=users)


def add_user_to_role(db: Session, id: int, request: schemas.AddById):
    user = db.query(models.User).filter(models.User.id == request.id).first()
    role = db.query(models.Role).options(joinedload(models.Role.users)).filter(models.Role.id == id).first()

    if not (user and role):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {request.id} or Role with id: {id} not found")
    
    role.users.append(user)
    db.commit()
    db.refresh(role)

    users = [schemas.ShowUser.from_orm(u) for u in role.users]

    return schemas.RoleUsers(id=role.id, name=role.name, code=role.code, description=role.description, users=users)


def remove_user_from_role(db: Session, id: int, request: schemas.AddById):
    role = db.query(models.Role).options(joinedload(models.Role.users)).filter(models.Role.id == id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id: {id} not found")
    
    user = db.query(models.User).filter(models.User.id == request.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {request.id} not found")
    
    if user not in role.users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Role does not have this user assigned")
    
    role.users.remove(user)
    db.commit()
    db.refresh(user)

    return {'details': 'User removed'}


############################################################################################################################################################################################
# PILOTS

def get_roles_pilots(db: Session, id: int):
    role = db.query(models.Role).filter(models.Role.id == id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id {id} not found")
    pilots = [schemas.ShowPilot.from_orm(p) for p in role.pilots]
    return schemas.RolePilots(id=role.id, name=role.name, code=role.code, description=role.description, pilots=pilots)


def add_pilot_to_role(db: Session, id: int, request: schemas.AddById):
    pilot = db.query(models.Pilot).filter(models.Pilot.id == request.id).first()
    role = db.query(models.Role).options(joinedload(models.Role.users)).filter(models.Role.id == id).first()
    if not (pilot and role):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id: {request.id} or Role with id: {id} not found")
    
    role.pilots.append(pilot)
    db.commit()
    db.refresh(role)

    pilots = [schemas.ShowPilot.from_orm(p) for p in role.pilots]

    return schemas.RolePilots(id=role.id, name=role.name, code=role.code, description=role.description, pilots=pilots)


def remove_pilot_from_role(db: Session, id: int, request: schemas.AddById):
    role = db.query(models.Role).options(joinedload(models.Role.pilots)).filter(models.Role.id == id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id: {id} not found")
    
    pilot = db.query(models.Pilot).filter(models.Pilot.id == request.id).first()
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id: {request.id} not found")
    
    if pilot not in role.pilots:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Role does not have this pilot assigned")
    
    role.pilots.remove(pilot)
    db.commit()
    db.refresh(role)

    return {'details': 'Pilot removed'}
