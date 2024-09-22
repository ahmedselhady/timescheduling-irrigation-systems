import sys

sys.path.append("d:\irrigation-project\.venv\lib\site-packages")

from fastapi import FastAPI
from utils.database import Base, engine
from routes.authentication import router as authentication_router
from routes.irrigation_scheduling import router as irrigation_scheduling_router
from models.user import UserDB

app = FastAPI()

# Create the tables in the database
Base.metadata.create_all(bind=engine)

app.include_router(authentication_router)
app.include_router(irrigation_scheduling_router)
