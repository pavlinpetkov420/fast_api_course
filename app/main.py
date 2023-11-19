from fastapi import FastAPI
from .routers import posts, users, auth, vote

from fastapi.middleware.cors import CORSMiddleware
########################################################################################################################
# TODO: 1.Go over the code in the project and add documentation

########################################################################################################################
# Command commented out because of alembic
# models.Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI()

origins: list[str] = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # What domains API is able to talk to? e.g. google.com
    allow_credentials=True,
    allow_methods=['*'],  # HTTP Methods => * = all
    allow_headers=['*']

)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Welcome to myAPI!"}