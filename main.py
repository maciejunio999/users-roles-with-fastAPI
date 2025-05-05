from fastapi import FastAPI
import models
from database import engine
from routers import endpoint, user, role, pilot, authentication, module, menu, product
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(engine)

app.include_router(menu.router)
app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(role.router)
app.include_router(pilot.router)
app.include_router(module.router)
app.include_router(endpoint.router)
app.include_router(product.router)