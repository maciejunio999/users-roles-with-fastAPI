from fastapi import APIRouter, Depends
import schemas, database, models, hashing
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from datetime import timedelta
from routers import JWT_token
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    tags=['Authentication']
)


@router.post('/token', response_model=schemas.Token)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    if not hashing.Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")
    
    access_token_expires = timedelta(minutes=JWT_token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = JWT_token.create_access_token(
        data={"sub": user.email, "roles": [role.code for role in user.roles]},
        expires_delta=access_token_expires
    )

    return schemas.Token(access_token=access_token, token_type="bearer")