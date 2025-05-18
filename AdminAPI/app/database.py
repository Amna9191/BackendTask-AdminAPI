import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1) Load .env into os.environ
load_dotenv()

DB_USER     = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_PORT     = os.getenv("DB_PORT", "3306")
DB_NAME     = os.getenv("DB_NAME", "ecommerce_admin_api")

# Build URLs
URL_WITHOUT_DB = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"
DATABASE_URL   = f"{URL_WITHOUT_DB}/{DB_NAME}?charset=utf8mb4"

# 2) Create the database itself if it doesn't exist
engine_tmp = create_engine(URL_WITHOUT_DB, pool_pre_ping=True)
with engine_tmp.connect() as conn:
    # COMMIT before running DDL on some MySQL setups
    conn.execute(text("COMMIT"))
    conn.execute(
        text(
            f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
    )

# 3) Now bind to the real database
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
