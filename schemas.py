from pydantic import BaseModel
from typing import List


class AddById(BaseModel):
    id: int


############################################################################################################################################################################################
# ROLES

class CreateRole(BaseModel):
    name: str
    code: str
    description: str

class ShowRole(CreateRole):
    id: int


############################################################################################################################################################################################
# PILOTS

class CreatePilot(BaseModel):
    name: str
    code: str
    description: str

class ShowPilot(CreatePilot):
    id: int
    state: bool

class UpdatePilotState(BaseModel):
    state: bool


############################################################################################################################################################################################
# MODULES

class CreateModule(BaseModel):
    name: str
    description: str

class FullModule(CreateModule):
    id: int
    name: str
    description: str
    in_config: bool

class Module(CreateModule):
    in_config: bool

class ModulePilot(Module):
    pilots: List[ShowPilot] = []
    class Config:
        from_attributes  = True


############################################################################################################################################################################################
# USERS

class ShowUser(BaseModel):
    username: str
    email: str


class User(BaseModel):
    username: str
    email: str
    password: str

class UserInDB(User):
    hashed_password: str

class UserId(ShowUser):
    id: int

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class UserRoles(UserId):
    roles: List[ShowRole] = []
    class Config:
        from_attributes  = True

class UserPilots(UserId):
    pilots: List[ShowPilot] = []
    class Config:
        from_attributes  = True


############################################################################################################################################################################################
# ROLES + REST

class RolePilots(ShowRole):
    pilots: List[ShowPilot] = []
    class Config:
        from_attributes  = True

class RoleUsers(ShowRole):
    owners: List[ShowUser] = []
    class Config:
        from_attributes  = True


############################################################################################################################################################################################
# PILOTS + REST

class PilotRoles(ShowPilot):
    roles: List[ShowRole] = []
    class Config:
        from_attributes  = True

class PilotUsers(ShowPilot):
    users: List[ShowUser] = []
    class Config:
        from_attributes  = True


############################################################################################################################################################################################
# SHOW FULL

class ShowFullUser(ShowUser):
    roles: List[ShowRole] = []
    pilots: List[ShowPilot] = []
    class Config:
        from_attributes  = True

class ShowFullModule(FullModule):
    roles: List[ShowRole] = []
    pilots: List[ShowPilot] = []
    class Config:
        from_attributes  = True

class ShowFullRole(ShowRole):
    owners: List[ShowUser] = []
    pilots: List[ShowPilot] = []
    class Config:
        from_attributes = True

class ShowFullPilot(ShowPilot):
    users: List[ShowUser] = []
    roles: List[ShowRole] = []
    class Config:
        from_attributes = True