from sqlalchemy.orm import Session, joinedload
import models, schemas
from fastapi import status, HTTPException
from typing import List


def get_all(db: Session):
    pilots = db.query(models.Pilot).all()
    print(pilots)
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


def update_pilot(db: Session, id: int, request: schemas.ShowPilot):
    pilot = db.query(models.Pilot).filter(models.Pilot.id == id).first()

    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pilot with id {id} not found")
    
    pilot.name = request.name
    pilot.code = request.code
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
