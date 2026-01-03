from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# الاتصال بقاعدة البيانات SQLite (يمكنك تغييرها لـ PostgreSQL أو غيرها)
DATABASE_URL = "sqlite:///./blog.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# دالة Dependency لاستخدامها في FastAPI
def get_db():
    """
    دالة تستخدم مع Depends للحصول على جلسة قاعدة البيانات.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
