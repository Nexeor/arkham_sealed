from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Configure Flask-SQLAlchemy with database
DATABASE_URL = "sqlite:///arkham.db" 
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create SQLAlchemy instance
db = SQLAlchemy(app)

# SQLAlchemy CORE setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() 

def init_db():
    """Create tables in the database if they do not exist."""
    Base.metadata.create_all(bind=engine)
