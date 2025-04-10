from fastapi import FastAPI
import models
from database import engine
from routers import endpoint, user, role, pilot, authentication, module, menu, product


app = FastAPI()


models.Base.metadata.create_all(engine)

app.include_router(menu.router)
app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(role.router)
app.include_router(pilot.router)
app.include_router(module.router)
app.include_router(endpoint.router)
app.include_router(product.router)