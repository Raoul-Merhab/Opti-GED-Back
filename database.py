from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, text
from sqlalchemy.orm.session import Session
from fastapi import Depends
from utils.Creds import DatabaseCreds

engine = create_engine(DatabaseCreds["Link"],
    echo=True
)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()