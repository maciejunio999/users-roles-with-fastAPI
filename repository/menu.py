from sqlalchemy.orm import Session, joinedload
import models
from fastapi import status, HTTPException


def get_menu(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no such user")
    
    user_pilots = [pilot for pilot in user.pilots if pilot.state == True]
    
    modules = db.query(models.Module).filter(models.Module.in_config == True).all()

    modules_in_menu = []

    for module in modules:
        if not module.pilots:
            modules_in_menu.append(module)
            break
        if any(pilot in user_pilots for pilot in module.pilots):
            modules_in_menu.append(module)
        else:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Something really weird occurred"
            )

    if not modules_in_menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no modules in menu")

    return modules_in_menu
