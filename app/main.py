from fastapi import FastAPI
from pydantic import BaseSettings

import app.models as models
from .database import engine
from .routers import posts, users, auth, vote
from .config import settings

########################################################################################################################
# TODO: 1.Go over the code in the project and add documentation

########################################################################################################################
# Command commented out because of alembic
# models.Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Welcome to myAPI!"}