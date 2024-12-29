from pydantic import BaseModel
from typing import List


class BaseUser(BaseModel):
    username: str
    email: str
    password: str


class User(BaseModel):
    username: str
    email: str
    class Config:
        orm_mode = True


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