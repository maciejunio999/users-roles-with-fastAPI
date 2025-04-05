from fastapi import Depends, HTTPException, status
import schemas
from oauth2 import get_current_user


def require_roles(*required_roles: str):
    def checker(current_user: schemas.TokenData = Depends(get_current_user)):
        if not set(required_roles).issubset(set(current_user.roles)):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return checker
