from sqlalchemy.orm import Session, joinedload
import models, schemas
from fastapi import status, HTTPException
from typing import List


############################################################################################################################################################################################
# BASIC

def get_all(db: Session):
    products = db.query(models.Product).all()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is none")
    return products


def get_one(db: Session, id: int):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} not found")
    print(product.id, product.name, product.description, product.state)
    return product


def create(request: schemas.CreateRole, db: Session):
    new_product = models.Product(name=request.name, description=request.description)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def update_role(db: Session, id: int, request: schemas.CreateRole):
    product = db.query(models.Product).filter(models.Product.id == id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} not found")
    
    product.name = request.name
    product.description = request.description
    db.commit()
    db.refresh(product)

    return schemas.ShowRole(id=product.id, name=product.name, description=product.description)


def delete(db: Session, id: int):
    product_query = db.query(models.Product).filter(models.Product.id == id)
    product = product_query.first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} not found")
    
    product_query.delete(synchronize_session=False)
    db.commit()
    return {'details': 'Product Deleted'}


############################################################################################################################################################################################
# ACTIVATION

def activate_product(db: Session, id: int):
    product = db.query(models.Product).filter(models.Product.id == id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} not found")
    if product.state:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product with id {id} is already active")
    
    product.state = True
    db.commit()
    db.refresh(product)

    return product


def deactivate_product(db: Session, id: int):
    product = db.query(models.Product).filter(models.Product.id == id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} not found")
    if not product.state:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product with id {id} is not active")
    
    product.state = False
    db.commit()
    db.refresh(product)

    return product