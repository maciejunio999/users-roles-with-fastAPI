from pydantic import BaseModel
from typing import List


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


class UpdateUserRole(BaseModel):
    role_id: int
    class Config:
        from_attributes = True


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


class RoleName(BaseModel):
    name: str


class UserRoles(BaseModel):
    id: int
    username: str
    roles: List[RoleName] = []
    class Config:
        from_attributes  = True


class RoleUsers(BaseModel):
    id: int
    name: str
    owners: List[User] = []
    class Config:
        from_attributes = True


class ShowRole(BaseModel):
    id: int
    code: str
    name: str
    class Config:
        from_attributes=True


class CreateRole(BaseModel):
    name: str
    code: str
    class Config:
        from_attributes = True


class AddUserToRole(BaseModel):
    user_id: int


class AddPilotToRole(BaseModel):
    pilot_id: int


class ShowFullPilot(BaseModel):
    id: int
    name: str
    code: str
    users: List[User] = []
    roles: List[ShowRole] = []
    class Config:
        from_attributes = True


class ShowPilot(BaseModel):
    name: str
    code: str
    class Config:
        from_attributes = True


class AddRoleToPilot(BaseModel):
    role_id: int


class ShowPilotAndRoles(BaseModel):
    name: str
    roles: List[ShowRole]
    class Config:
        from_attributes = True


class RolePilots(BaseModel):
    id: int
    name: str
    pilots: List[ShowPilot] = []
    class Config:
        from_attributes = True


class ShowPilotAndUsers(BaseModel):
    name: str
    users: List[ShowUser]
    class Config:
        from_attributes = True


class AddUserToPilot(BaseModel):
    user_id: int


class PilotRoles(BaseModel):
    id: int
    name: str
    roles: List[ShowRole] = []
    class Config:
        from_attributes = True


class PilotUsers(BaseModel):
    id: int
    name: str
    users: List[ShowUser] = []
    class Config:
        from_attributes = True


class ShowFullRole(BaseModel):
    id: int
    name: str
    code: str
    owners: List[User] = []
    pilots: List[ShowPilot] = []
    class Config:
        from_attributes = True