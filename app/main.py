from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import app.models as models
from .database import engine
from .routers import posts, users, auth


########################################################################################################################
# TODO: 1.Go over the code in the project and add documentation

########################################################################################################################
models.Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI()


try:
    connection = psycopg2.connect(host='localhost', database='fast_api', user='postgres',
                                    password='J0Gj_cLZTaCH0FqweV^O1A', cursor_factory=RealDictCursor)
    cursor = connection.cursor()
    print("Database connection was successful!")
except Exception as ex:
    raise Exception(ex)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Welcome to myAPI!"}