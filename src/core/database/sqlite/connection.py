from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import CONFIG
from contextlib import contextmanager

SQLALCHEMY_DATABASE_URL = f"sqlite:///{CONFIG.DB_SQLITE_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def sqlite_connection():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
    finally:
        db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
    finally:
        db.close()