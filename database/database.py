from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DB_USER = os.environ.get("DB_USER")

Base = declarative_base()

engine = create_engine("postgresql://postgres:1234@localhost:5432/Logistic Management")

session = sessionmaker(bind=engine)

