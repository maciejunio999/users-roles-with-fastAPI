from fastapi import FastAPI
import models
from database import engine
from routers import user, role, authentication


app = FastAPI()


models.Base.metadata.create_all(engine)


app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(role.router)
