from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL
DATABASE_URL = "sqlite:///./irrigation.db"

# Create a database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a base class for ORM models
BaseDbEntity = declarative_base()

# Create a session local class for database access
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
