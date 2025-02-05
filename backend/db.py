from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Database URL (adjust according to your setup)
DATABASE_URL = "sqlite:///example.db" 

# Create engine and bind it to Base
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine, checkfirst=True)  # Creates the tables

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)