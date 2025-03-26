from sqlalchemy.orm import Session
import models, schemas, hashing
from fastapi import status, HTTPException


############################################################################################################################################################################################
# BASIC

def get_all(db: Session):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is none")
    return users


def get_one(db: Session, id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user


def create(request: schemas.User, db: Session):
    new_user = models.User(username=request.username, email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def delete(db: Session, id: int):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    
    user_query.delete(synchronize_session=False)
    db.commit()
    return {'details': 'User Deleted'}


def update(db: Session, id: int, request: schemas.User):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    
    user.username = request.username
    user.email = request.email
    user.password = request.password
    db.commit()
    db.refresh(user)

    return {'details': 'User Updated'}


############################################################################################################################################################################################
# ROLES

def get_users_roles(db: Session, id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user


def add_role_to_user(db: Session, id: int, request: schemas.AddById):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")

    role = db.query(models.Role).filter(models.Role.id == request.id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id: {request.id} not found")
    if role in user.roles:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User already has this role")

    user.roles.append(role)
    db.commit()
    db.refresh(user)

    return user


def remove_role_from_user(db: Session, id: int, request: schemas.AddById):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")

    role = db.query(models.Role).filter(models.Role.id == request.id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id: {request.id} not found")

    if role not in user.roles:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User does not have this role")

    user.roles.remove(role)
    
    db.commit()
    db.refresh(user)

    user_roles = [schemas.CreateRole(name=role.name) for role in user.roles]

    return schemas.UserRoles(id=user.id, username=user.username, roles=user_roles)


############################################################################################################################################################################################
# PILOTS

def get_users_pilots(db: Session, id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user


def get_users_active_pilots(db: Session, id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")

    user_active_pilots = [schemas.ShowPilot(name=pilot.name) for pilot in user.pilots if pilot.state == True]

    return schemas.UserPilots(id=user.id, username=user.username, pilots=user_active_pilots)


def add_pilot_to_user(db: Session, id: int, request: schemas.AddById):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")

    pilot = db.query(models.Pilot).filter(models.Pilot.id == request.id).first()
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id: {request.id} not found")

    user.pilots.append(pilot)

    for role in pilot.roles:
        if role in user.roles:
            pass
        else:
            user.roles.append(role)

    db.commit()
    db.refresh(user)

    return user


def remove_pilot_from_user(db: Session, id: int, request: schemas.AddById):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")

    pilot = db.query(models.Pilot).filter(models.Pilot.id == request.id).first()
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id: {request.id} not found")

    if pilot not in user.pilots:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User does not have this pilot")

    user.pilots.remove(pilot)
    
    db.commit()
    db.refresh(user)

    return {'details': 'Pilot removed'}