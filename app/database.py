from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# template: <driver_type>://<username>:<password>:<ip_adress/hostname>/<database_name>
SQL_ALCHEMY_DB_URL: str = "postgresql+psycopg2://postgres:J0Gj_cLZTaCH0FqweV^O1A@localhost:5432/fast_api"

engine = create_engine(SQL_ALCHEMY_DB_URL)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Every time when have a request, will create a session
    execute the request and close the session
    :yield: Database Session
    """
    db = session()
    try:
        yield db
    finally:
        db.close()

# This block was used before ORM
# while True:
#     try:
#         connection = psycopg2.connect(host='localhost', database='fast_api', user='postgres',
#                                       password='J0Gj_cLZTaCH0FqweV^O1A', cursor_factory=RealDictCursor)
#         cursor = connection.cursor()
#         print("Database connection was successful!")
#     except Exception as ex:
#         raise Exception(ex)