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
    class Config:
        from_attributes  = True

class ShowRole(CreateRole):
    id: int

class RoleCode(BaseModel):
    code: str
    class Config:
        from_attributes  = True

############################################################################################################################################################################################
# PILOTS

class CreatePilot(BaseModel):
    name: str
    code: str
    description: str
    class Config:
        from_attributes  = True

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


############################################################################################################################################################################################
# ENDPOINTS

class CreateEndpoint(BaseModel):
    name: str
    url: str
    description: str
    class Config:
        from_attributes  = True

class HttpMethod(BaseModel):
    http_method: str

class ShowEndpoint(CreateModule):
    id: int
    http_method: str


############################################################################################################################################################################################
# USERS

class ShowUser(BaseModel):
    username: str
    email: str
    class Config:
        from_attributes  = True

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
    roles: List[str] | None = None

class UserRoles(UserId):
    roles: List[ShowRole] = []

class UserPilots(UserId):
    pilots: List[ShowPilot] = []

############################################################################################################################################################################################
# ROLES + REST

class RolePilots(ShowRole):
    pilots: List[ShowPilot] = []

class RoleUsers(ShowRole):
    users: List[ShowUser] = []


############################################################################################################################################################################################
# PILOTS + REST

class PilotRoles(ShowPilot):
    roles: List[ShowRole] = []

class PilotUsers(ShowPilot):
    users: List[ShowUser] = []


############################################################################################################################################################################################
# SHOW FULL

class ShowFullUser(ShowUser):
    roles: List[ShowRole] = []
    pilots: List[ShowPilot] = []
    class Config:
        from_attributes  = True

class ShowFullModule(FullModule):
    pilots: List[ShowPilot] = []
    class Config:
        from_attributes  = True

class ShowFullRole(ShowRole):
    users: List[ShowUser] = []
    pilots: List[ShowPilot] = []

class ShowFullPilot(ShowPilot):
    users: List[ShowUser] = []
    roles: List[ShowRole] = []

class ShowFullEndpoint(ShowEndpoint):
    modules: List[FullModule] = []