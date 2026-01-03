import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Use env var if set, otherwise use a local sqlite file for development
env_url = os.getenv("DATABASE_URL")
DATABASE_URL = env_url if env_url not in (None, "") else "sqlite:///./test.db"

# sqlite needs check_same_thread; other DBs don't accept that kwarg
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
