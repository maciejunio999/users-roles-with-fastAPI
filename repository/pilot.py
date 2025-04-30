from sqlalchemy.orm import Session, joinedload
import models, schemas
from fastapi import status, HTTPException
from typing import List


############################################################################################################################################################################################
# BASIC

def get_all(db: Session):
    pilots = db.query(models.Pilot).all()
    if not pilots:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is none")
    return pilots


def get_one(db: Session, id: int):
    pilot = db.query(models.Pilot).filter(models.Pilot.id == id).first()
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id {id} not found")
    return pilot


def create(request: schemas.CreatePilot, db: Session):
    if len(db.query(models.Pilot).filter(models.Pilot.name == request.name).all()) >= 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"This name is already taken")
    
    if len(db.query(models.Pilot).filter(models.Pilot.code == request.code).all()) >= 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"This code is already taken")
    new_pilot = models.Pilot(name=request.name, code=request.code, description=request.description)
    db.add(new_pilot)
    db.commit()
    db.refresh(new_pilot)
    return new_pilot


def delete(db: Session, id: int):
    pilot_query = db.query(models.Pilot).filter(models.Pilot.id == id)
    user = pilot_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id {id} not found")
    
    pilot_query.delete(synchronize_session=False)
    db.commit()
    return {'details': 'Pilot Deleted'}


def update_pilot(db: Session, id: int, request: schemas.CreatePilot):
    pilot = db.query(models.Pilot).filter(models.Pilot.id == id).first()

    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id {id} not found")
    
    if len(db.query(models.Pilot).filter(models.Pilot.name == request.name).all()) >= 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"This name is already taken")
    
    if len(db.query(models.Pilot).filter(models.Pilot.code == request.code).all()) >= 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"This code is already taken")
    
    pilot.name = request.name
    pilot.code = request.code
    db.commit()
    db.refresh(pilot)

    return pilot


############################################################################################################################################################################################
# ACTIVATION

def activate_pilot(db: Session, id: int):
    pilot = db.query(models.Pilot).filter(models.Pilot.id == id).first()

    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id {id} not found")
    if pilot.state:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Pilot with id {id} is already active")
    
    pilot.state = True
    db.commit()
    db.refresh(pilot)

    return pilot


def deactivate_pilot(db: Session, id: int):
    pilot = db.query(models.Pilot).filter(models.Pilot.id == id).first()

    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id {id} not found")
    if not pilot.state:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Pilot with id {id} is not active")
    
    pilot.state = False
    db.commit()
    db.refresh(pilot)

    return pilot


############################################################################################################################################################################################
# ROLES

def get_pilots_roles(db: Session, id: int):
    pilot = db.query(models.Pilot).filter(models.Pilot.id == id).first()

    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id {id} not found")
    
    roles = [schemas.ShowRole.from_orm(r) for r in pilot.roles]

    return schemas.PilotRoles(id=pilot.id, name=pilot.name, code=pilot.code, description=pilot.description, state=pilot.state, roles=roles)


def add_role_to_pilot(db: Session, id: int, request: schemas.AddById):
    pilot = db.query(models.Pilot).filter(models.Pilot.id == id).first()
    role = db.query(models.Role).filter(models.Role.id == request.id).first()
    
    if not (pilot and role):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id: {id} or Role with id: {request.id} not found")

    if role not in pilot.roles:
        pilot.roles.append(role)
        db.commit()
        db.refresh(pilot)

    roles = [schemas.ShowRole.from_orm(r) for r in pilot.roles]

    return schemas.PilotRoles(id=pilot.id, name=pilot.name, code=pilot.code, description=pilot.description, state=pilot.state, roles=roles)


def remove_role_from_pilot(db: Session, id: int, request: schemas.AddById):
    pilot = db.query(models.Pilot).options(joinedload(models.Pilot.roles)).filter(models.Pilot.id == id).first()
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id: {request.id} not found")
    
    role = db.query(models.Role).filter(models.Role.id == request.id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id: {request.id} not found")
    
    if role not in pilot.roles:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Pilot does not have this role assigned")
    
    pilot.roles.remove(role)
    db.commit()
    db.refresh(pilot)

    return {'details': 'Role Deleted'}


############################################################################################################################################################################################
# USERS

def get_pilots_users(db: Session, id: int):
    pilot = db.query(models.Pilot).filter(models.Pilot.id == id).first()
    
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id {id} not found")
    
    users = [schemas.ShowUser.from_orm(u) for u in pilot.users]

    return schemas.PilotUsers(id=pilot.id, name=pilot.name, code=pilot.code, description=pilot.description, state=pilot.state, users=users)


def add_user_to_pilot(db: Session, id: int, request: schemas.AddById):
    pilot = db.query(models.Pilot).filter(models.Pilot.id == id).first()
    user = db.query(models.User).filter(models.User.id == request.id).first()
    
    if not (pilot and user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id: {id} or User with id: {request.id} not found")

    if user not in pilot.users:
        pilot.users.append(user)

        user_role_ids = {r.id for r in user.roles}

        for role in pilot.roles:
            if role.id not in user_role_ids:
                user.roles.append(role)

        db.commit()
        db.refresh(user)
        db.refresh(pilot)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Pilot with id: {id} is assigned to User with id: {request.id}")

    users = [schemas.ShowUser.from_orm(u) for u in pilot.users]

    return schemas.PilotUsers(id=pilot.id, name=pilot.name, code=pilot.code, description=pilot.description, state=pilot.state, users=users)


def remove_user_from_pilot(db: Session, id: int, request: schemas.AddById):
    pilot = db.query(models.Pilot).options(joinedload(models.Pilot.users)).filter(models.Pilot.id == id).first()
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id: {request.id} not found")
    
    user = db.query(models.User).filter(models.User.id == request.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {request.id} not found")
    
    if user not in pilot.users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Pilot does not have this user assigned")
    
    pilot.users.remove(user)
    db.commit()
    db.refresh(pilot)

    return {'details': 'Role Deleted'}