from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL
DATABASE_URL = "sqlite:///./irrigation.db"

# Create a database engine
db_engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a base class for ORM models
base_db_entity = declarative_base()

# Create a session local class for database access
local_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)


# Dependency for database session
def get_db_session():
    db = local_session()
    try:
        yield db
    finally:
        db.close()
