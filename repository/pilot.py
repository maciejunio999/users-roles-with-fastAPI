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


def create(request: schemas.CreatePilot, db: Session):
    new_pilot = models.Pilot(name=request.name, code=request.code)
    db.add(new_pilot)
    db.commit()
    db.refresh(new_pilot)
    return new_pilot