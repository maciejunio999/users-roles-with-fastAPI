from sqlalchemy.orm import Session
import models, schemas
from fastapi import status, HTTPException


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
    
    module.name = request.name
    module.description = request.description
    db.commit()
    db.refresh(module)

    return {'details': 'Module Updated'}