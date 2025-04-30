from sqlalchemy.orm import Session
import models, schemas
from fastapi import status, HTTPException


############################################################################################################################################################################################
# BASIC

def get_all(db: Session):
    modules = db.query(models.Module).all()
    if not modules:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is none")
    return modules


def get_one(db: Session, id: int):
    module = db.query(models.Module).filter(models.Module.id == id).first()
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Module with id {id} not found")
    return module


def create(request: schemas.CreateModule, db: Session):
    if len(db.query(models.Module).filter(models.Module.name == request.name).all()) >= 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"This name is already taken")
    
    if len(db.query(models.Module).filter(models.Module.code == request.code).all()) >= 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"This code is already taken")
    
    new_module = models.Module(name=request.name, description=request.description)
    db.add(new_module)
    db.commit()
    db.refresh(new_module)
    return new_module


def delete(db: Session, id: int):
    module_query = db.query(models.Module).filter(models.Module.id == id)
    module = module_query.first()

    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Module with id {id} not found")
    
    module_query.delete(synchronize_session=False)
    db.commit()
    return {'details': 'Module Deleted'}


def update(db: Session, id: int, request: schemas.CreateModule):
    module = db.query(models.Module).filter(models.Module.id == id).first()

    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Module with id {id} not found")
    
    if len(db.query(models.Module).filter(models.Module.name == request.name).all()) >= 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"This name is already taken")
    
    if len(db.query(models.Module).filter(models.Module.code == request.code).all()) >= 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"This code is already taken")
    
    module.name = request.name
    module.description = request.description
    db.commit()
    db.refresh(module)

    return {'details': 'Module Updated'}


############################################################################################################################################################################################
# ACTIVATION

def activate_module(db: Session, id: int):
    module = db.query(models.Module).filter(models.Module.id == id).first()

    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Module with id {id} not found")
    if module.in_config:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Module with id {id} is already active")
    
    module.in_config = True
    db.commit()
    db.refresh(module)

    return module


def deactivate_module(db: Session, id: int):
    module = db.query(models.Module).filter(models.Module.id == id).first()

    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Module with id {id} not found")
    if not module.in_config:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Module with id {id} is not active")
    
    module.in_config = False
    db.commit()
    db.refresh(module)

    return module


############################################################################################################################################################################################
# PILOTS

def add_pilot_to_module(db: Session, id: int, request: schemas.AddById):
    module = db.query(models.Module).filter(models.Module.id == id).first()
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Module with id: {id} not found")

    pilot = db.query(models.Pilot).filter(models.Pilot.id == request.id).first()
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id: {request.id} not found")
    
    if pilot not in module.pilots:
        module.pilots.append(pilot)
        db.commit()
        db.refresh(pilot)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Module with id: {id} already has Pilot with id: {request.id}")

    return module


def remove_pilot_from_module(db: Session, id: int, request: schemas.AddById):
    module = db.query(models.Module).filter(models.Module.id == id).first()
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Module with id: {id} not found")

    pilot = db.query(models.Pilot).filter(models.Pilot.id == request.id).first()
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id: {request.id} not found")

    if pilot not in module.pilots:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Module does not have this pilot")

    module.pilots.remove(pilot)
    db.commit()
    db.refresh(module)

    return {'details': 'Pilot removed'}


def get_modules_pilots(db: Session, id: int):
    module = db.query(models.Module).filter(models.Module.id == id).first()
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return module


def get_modules_active_pilots(db: Session, id: int):
    module = db.query(models.Module).filter(models.Module.id == id).first()
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    
    module_active_pilots = [schemas.PilotName(name=pilot.name) for pilot in module.pilots if pilot.state == True]

    return schemas.ShowFullModule(name=module.name, description=module.description, in_config = module.in_config, pilots=module_active_pilots)
