from sqlalchemy import create_backend, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite akan otomatis membuat file bernama 'keuangan.db' di folder Anda
SQLALCHEMY_DATABASE_URL = "sqlite:///./keuangan.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency untuk mendapatkan koneksi database saat API dipanggil
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()