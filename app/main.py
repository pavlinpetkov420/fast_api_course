from fastapi import FastAPI
import app.models as models
from .database import engine
from .routers import posts, users, auth


########################################################################################################################
# TODO: 1.Go over the code in the project and add documentation

########################################################################################################################
models.Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Welcome to myAPI!"}