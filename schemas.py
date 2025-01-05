from pydantic import BaseModel
from typing import List


class BaseUser(BaseModel):
    username: str
    email: str
    password: str


class User(BaseModel):
    id: int
    username: str
    email: str
    class Config:
        from_attributes  = True


class UserInDB(User):
    hashed_password: str


class UpdateUser(BaseModel):
    username: str
    email: str


class ShowUser(BaseModel):
    username: str
    email: str
    class Config:
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class ShowRole(BaseModel):
    name: str
    owners: List[User] = []
    class Config:
        from_attributes = True


class CreateRole(BaseModel):
    name: str
    code: str


class AddUserToRole(BaseModel):
    user_id: int