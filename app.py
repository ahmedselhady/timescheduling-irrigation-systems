import sys

sys.path.append("d:\irrigation-project\.venv\lib\site-packages")

from fastapi import FastAPI
from utils.database import BaseDbEntity, db_engine
from routes.authentication import router as authentication_router
from routes.irrigation_scheduling import router as irrigation_scheduling_router
from models.user import UserDB

app = FastAPI()

# Create the tables in the database
BaseDbEntity.metadata.create_all(bind=db_engine)

app.include_router(authentication_router)
app.include_router(irrigation_scheduling_router)
