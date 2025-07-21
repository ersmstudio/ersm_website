from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# تحميل المتغيرات من ملف .env
load_dotenv()

# الحصول على رابط الاتصال بقاعدة البيانات
DATABASE_URL = os.getenv("DATABASE_URL")

# التحقق من أن الرابط موجود
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env")

# إنشاء المحرك (engine)
engine = create_engine(DATABASE_URL)

# إنشاء جلسة للتعامل مع قواعد البيانات
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# القاعدة الأساسية للنماذج (Models)
Base = declarative_base()
