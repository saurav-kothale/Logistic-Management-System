from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from decouple import config
from sqlalchemy.exc import PendingRollbackError
from app import setting

USER_NAME = setting.DB_USER_NAME
DB_PASSWORD = setting.DB_PASSWORD
DB_PORT = setting.DB_PORT
DB_NAME = setting.DB_NAME
DB_HOST = setting.DB_HOST

connection_string = (
    f"postgresql://{USER_NAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

Base = declarative_base()

engine = create_engine(connection_string, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except PendingRollbackError:
        db.rollback()
        raise
    finally:
        db.close()
