import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

PG_HOST = os.getenv("PG_HOST") or "localhost"
PG_PORT = os.getenv("PG_PORT") or 5432
PG_USER = os.getenv("PG_USER") or "postgres"
PG_PASSWORD = os.getenv("PG_PASSWORD") or "pgpass"
PG_DB = os.getenv("PG_DB") or "rinha_db"
PG_POOL = int(os.getenv("PG_POOL") or 10)

SQLALCHEMY_DATABASE_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=PG_POOL, max_overflow=0)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()