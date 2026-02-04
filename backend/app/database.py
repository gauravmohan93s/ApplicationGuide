from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Fallback for local testing if not set, though Railway will provide it.
# If you want to use a local sqlite for dev, you can un-comment:
# if not DATABASE_URL:
#     DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL) if DATABASE_URL else None

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
