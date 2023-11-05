import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

current_directory = os.getcwd()

load_dotenv(current_directory + "/.env")

db_url = os.environ.get('DATABASE_URL')

engine = create_engine(db_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)