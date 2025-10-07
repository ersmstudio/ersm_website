# database.py

from sqlalchemy import create_engine
<<<<<<< Updated upstream
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# الاتصال بقاعدة البيانات SQLite (يمكنك تغييرها لـ PostgreSQL أو غيرها)
DATABASE_URL = "sqlite:///./blog.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
=======
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

# قراءة رابط قاعدة البيانات من البيئة
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ لم يتم العثور على DATABASE_URL في ملف .env")

# إنشاء محرك الاتصال بقاعدة البيانات
try:
    engine = create_engine(DATABASE_URL, echo=False, future=True)
except SQLAlchemyError as e:
    print(f"⚠️ خطأ في الاتصال بقاعدة البيانات: {e}")
    raise

# إعداد الجلسة Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# القاعدة الأساسية لبناء النماذج
>>>>>>> Stashed changes
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
