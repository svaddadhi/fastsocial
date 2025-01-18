import models

from database import engine
from fastapi import FastAPI
from routers import auth
from routers import comments
from routers import posts
from routers import relationships

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(relationships.router)
app.include_router(comments.router)
