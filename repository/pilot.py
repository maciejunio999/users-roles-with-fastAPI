from sqlalchemy.orm import Session, joinedload
import models, schemas
from fastapi import status, HTTPException
from typing import List


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


def create(request: schemas.ShowPilot, db: Session):
    new_pilot = models.Pilot(name=request.name, code=request.code)
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
    
    pilot.name = request.name
    pilot.code = request.code
    db.commit()
    db.refresh(pilot)

    return pilot


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


def add_role_to_pilot(db: Session, id: int, request: schemas.AddRoleToPilot):
    pilot = db.query(models.Pilot).filter(models.Pilot.id == id).first()
    role = db.query(models.Role).filter(models.Role.id == request.role_id).first()
    
    if not (pilot and role):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id: {id} or Role with id: {request.role_id} not found")

    if role not in pilot.roles:
        pilot.roles.append(role)
        db.commit()
        db.refresh(pilot)

    roles = [schemas.ShowRole.from_orm(r) for r in pilot.roles]

    return schemas.ShowPilotAndRoles(name=pilot.name, roles=roles)


def add_user_to_pilot(db: Session, id: int, request: schemas.AddUserToPilot):
    pilot = db.query(models.Pilot).filter(models.Pilot.id == id).first()
    user = db.query(models.User).filter(models.User.id == request.user_id).first()
    
    if not (pilot and user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id: {id} or User with id: {request.user_id} not found")

    if user not in pilot.users:
        pilot.users.append(user)
        db.commit()
        db.refresh(pilot)

    users = [schemas.ShowUser.from_orm(u) for u in pilot.users]

    return schemas.ShowPilotAndUsers(name=pilot.name, users=users)


def get_pilots_roles(db: Session, id: int):
    pilot = db.query(models.Pilot).filter(models.Pilot.id == id).first()
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id {id} not found")
    roles = [schemas.ShowRole.from_orm(r) for r in pilot.roles]
    return schemas.PilotRoles(id=pilot.id, name=pilot.name, roles=roles)


def get_pilots_users(db: Session, id: int):
    pilot = db.query(models.Pilot).filter(models.Pilot.id == id).first()
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id {id} not found")
    users = [schemas.ShowUser.from_orm(u) for u in pilot.users]
    return schemas.PilotUsers(id=pilot.id, name=pilot.name, users=users)


def remove_role_from_pilot(db: Session, id: int, request: schemas.AddRoleToPilot):
    pilot = db.query(models.Pilot).options(joinedload(models.Pilot.roles)).filter(models.Pilot.id == id).first()
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id: {request.id} not found")
    
    role = db.query(models.Role).filter(models.Role.id == request.role_id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id: {request.role_id} not found")
    
    if role not in pilot.roles:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Pilot does not have this role assigned")
    
    pilot.roles.remove(role)
    db.commit()
    db.refresh(pilot)

    roles = [schemas.ShowRole.from_orm(r) for r in pilot.roles]

    return schemas.ShowPilotAndRoles(name=pilot.name, roles=roles)


def remove_user_from_pilot(db: Session, id: int, request: schemas.AddUserToPilot):
    pilot = db.query(models.Pilot).options(joinedload(models.Pilot.users)).filter(models.Pilot.id == id).first()
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id: {request.id} not found")
    
    user = db.query(models.User).filter(models.User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {request.user_id} not found")
    
    if user not in pilot.users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Pilot does not have this user assigned")
    
    pilot.users.remove(user)
    db.commit()
    db.refresh(pilot)

    users = [schemas.ShowUser.from_orm(u) for u in pilot.users]

    return schemas.ShowPilotAndUsers(name=pilot.name, users=users)