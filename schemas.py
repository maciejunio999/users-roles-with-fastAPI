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
    role_id: int


############################################################################################################################################################################################
# PILOTS

class CretePilot(BaseModel):
    name: str
    code: str
    description: str

class ShowPilot(CretePilot):
    pilot_id: int
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


class UpdateModulesPilots(Module):
    pilot_id: int


class ModulePilot(Module):
    pilots: List[ShowPilot] = []
    class Config:
        from_attributes  = True


############################################################################################################################################################################################
# USERS

class UserId(BaseModel):
    id: int


class User(BaseModel):
    username: str
    email: str
    password: str


class UserInDB(User):
    hashed_password: str


class ShowUser(UserId):
    username: str
    email: str


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class UserRoles(ShowUser):
    roles: List[ShowRole] = []
    class Config:
        from_attributes  = True


class UserPilots(ShowUser):
    pilots: List[ShowPilot] = []
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