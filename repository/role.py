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
    return role


def get_roles_users(db: Session, id: int):
    role = db.query(models.Role).filter(models.Role.id == id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id {id} not found")
    owners = [schemas.User.from_orm(u) for u in role.users]
    return schemas.RoleUsers(id=role.id, name=role.name, owners=owners)


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


def delete(db: Session, id: int):
    role_query = db.query(models.Role).filter(models.Role.id == id)
    user = role_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id {id} not found")
    
    role_query.delete(synchronize_session=False)
    db.commit()
    return {'details': 'Role Deleted'}


def remove_user_from_role(db: Session, id: int, request: schemas.AddUserToRole):
    role = db.query(models.Role).options(joinedload(models.Role.users)).filter(models.Role.id == id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id: {request.role_id} not found")
    
    user = db.query(models.User).filter(models.User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
    
    if user not in role.users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Role does not have this user assigned")
    
    role.users.remove(user)
    db.commit()
    db.refresh(user)
    owners = [schemas.User.from_orm(u) for u in role.users]

    return schemas.ShowFullRole(id=role.id, name=role.name, code=role.code, owners=owners)