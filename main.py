from fastapi import FastAPI
import models
from database import engine
from routers import user, role, pilot, authentication, module, menu, test


app = FastAPI()


models.Base.metadata.create_all(engine)

app.include_router(test.router)
app.include_router(menu.router)
app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(role.router)
app.include_router(pilot.router)
app.include_router(module.router)
