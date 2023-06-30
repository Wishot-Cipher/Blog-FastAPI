from fastapi import FastAPI
from . import models
from .routers import user, post, authentication
from .database import engine

app = FastAPI()

models.Base.metadata.create_all(engine)


app.include_router(authentication.router)
app.include_router(post.router)
app.include_router(user.router)


