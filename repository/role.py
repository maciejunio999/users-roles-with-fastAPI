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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    owners = [schemas.User.from_orm(u) for u in role.users]
    return schemas.ShowRole(name=role.name, owners=owners)

def create(request: schemas.CreateRole, db: Session):
    new_role = models.Role(name=request.name, code=request.code)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

def add_user_to_role(db: Session, id: int, request: schemas.AddUserToRole):
    user = db.query(models.User).filter(models.User.id == request.user_id).first()
    role = db.query(models.Role).options(joinedload(models.Role.users)).filter(models.Role.id == id).first()
    if not (user and role):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {request.user_id} or Role with id: {id} not found")
    
    role.users.append(user)
    db.commit()
    db.refresh(role)

    owners = [schemas.User.from_orm(u) for u in role.users]

    return schemas.ShowRole(name=role.name, owners=owners)