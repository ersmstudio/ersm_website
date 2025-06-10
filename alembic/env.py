import os
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from sqlalchemy import MetaData
from alembic import context

# استيراد Base من models
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))
from models import Base  # غيّر هذا حسب مسار ملفك

# استخدم المتغير من البيئة
DATABASE_URL = os.getenv("DATABASE_URL")



# إعداد config
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# قم بتعيين الـ URL مباشرة هنا
config.set_main_option("sqlalchemy.url", DATABASE_URL)

target_metadata = Base.metadata
