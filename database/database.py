from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from decouple import config

USER_NAME = config("DB_USER_NAME")
DB_PASSWORD  = config("DB_PASSWORD")
DB_PORT = config("DB_PORT")
DB_NAME = config("DB_NAME")
DB_HOST = config("DB_HOST")

connection_string = f"postgresql://{USER_NAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


Base = declarative_base()

engine = create_engine(connection_string, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine)