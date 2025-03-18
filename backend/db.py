from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database URL (adjust according to your setup)
DATABASE_URL = "sqlite:///example.db" 

# Create engine and bind it to Base
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 

db = SessionLocal()

def init_db():
    """Create tables in the database if they do not exist."""
    Base.metadata.create_all(bind=engine)
