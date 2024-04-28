from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config import settings

POSTGRES_DATABASE_URL = URL.create(
    "postgresql+psycopg",
    username=settings.sql_username,
    password=settings.sql_password,
    host=settings.sql_hostname,
    database=settings.sql_db_name,
)
engine = create_engine(POSTGRES_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
