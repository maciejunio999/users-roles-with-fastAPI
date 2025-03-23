from sqlalchemy.orm import Session, joinedload
import models, schemas
from fastapi import status, HTTPException
from typing import List


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


def get_roles_users(db: Session, id: int):
    role = db.query(models.Role).filter(models.Role.id == id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id {id} not found")
    owners = [schemas.User.from_orm(u) for u in role.users]
    return schemas.RoleUsers(id=role.id, name=role.name, owners=owners)


def get_roles_pilots(db: Session, id: int):
    role = db.query(models.Role).filter(models.Role.id == id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id {id} not found")
    pilots = [schemas.ShowPilot.from_orm(u) for u in role.pilots]
    return schemas.RolePilots(id=role.id, name=role.name, pilots=pilots)


def create(request: schemas.CreateRole, db: Session):
    new_role = models.Role(name=request.name, code=request.code)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role


def update_role(db: Session, id: int, request: schemas.CreateRole):
    role = db.query(models.Role).filter(models.Role.id == id).first()

    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id {id} not found")
    
    role.name = request.name
    role.code = request.code
    db.commit()
    db.refresh(role)

    owners = [schemas.User.from_orm(u) for u in role.users]

    return schemas.ShowFullRole(id=role.id, name=role.name, code=role.code, owners=owners)


def add_user_to_role(db: Session, id: int, request: schemas.AddUserById):
    user = db.query(models.User).filter(models.User.id == request.user_id).first()
    role = db.query(models.Role).options(joinedload(models.Role.users)).filter(models.Role.id == id).first()
    if not (user and role):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {request.user_id} or Role with id: {id} not found")
    
    role.users.append(user)
    db.commit()
    db.refresh(role)

    owners = [schemas.User.from_orm(u) for u in role.users]
    pilots = [schemas.User.from_orm(p) for p in role.pilots]

    return schemas.ShowRole(name=role.name, owners=owners, pilots=pilots)


def add_pilot_to_role(db: Session, id: int, request: schemas.AddPilotById):
    pilot = db.query(models.Pilot).filter(models.Pilot.id == request.pilot_id).first()
    role = db.query(models.Role).options(joinedload(models.Role.users)).filter(models.Role.id == id).first()
    if not (pilot and role):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id: {request.pilot_id} or Role with id: {id} not found")
    
    role.pilots.append(pilot)
    db.commit()
    db.refresh(role)

    pilots = [schemas.ShowPilot.from_orm(p) for p in role.pilots]
    owners = [schemas.User.from_orm(u) for u in role.users]

    return schemas.ShowFullRole(id=role.id, name=role.name, code=role.code, owners=owners, pilots=pilots)


def delete(db: Session, id: int):
    role_query = db.query(models.Role).filter(models.Role.id == id)
    user = role_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    
    role_query.delete(synchronize_session=False)
    db.commit()
    return {'details': 'Role Deleted'}


def remove_user_from_role(db: Session, id: int, request: schemas.AddUserById):
    role = db.query(models.Role).options(joinedload(models.Role.users)).filter(models.Role.id == id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id: {id} not found")
    
    user = db.query(models.User).filter(models.User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {request.user_id} not found")
    
    if user not in role.users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Role does not have this user assigned")
    
    role.users.remove(user)
    db.commit()
    db.refresh(user)
    owners = [schemas.User.from_orm(u) for u in role.users]
    pilots = [schemas.ShowPilot.from_orm(u) for u in role.pilots]

    return schemas.ShowFullRole(id=role.id, name=role.name, code=role.code, owners=owners, pilots=pilots)


def remove_pilot_from_role(db: Session, id: int, request: schemas.AddPilotById):
    role = db.query(models.Role).options(joinedload(models.Role.pilots)).filter(models.Role.id == id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id: {id} not found")
    
    pilot = db.query(models.Pilot).filter(models.Pilot.id == request.pilot_id).first()
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id: {request.pilot_id} not found")
    
    if pilot not in role.pilots:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Role does not have this pilot assigned")
    
    role.pilots.remove(pilot)
    db.commit()
    db.refresh(role)
    pilots = [schemas.ShowPilot.from_orm(u) for u in role.pilots]
    owners = [schemas.User.from_orm(u) for u in role.users]

    return schemas.ShowFullRole(id=role.id, name=role.name, code=role.code, pilots=pilots, owners=owners)
