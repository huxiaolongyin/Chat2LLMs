from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from core.config import CONFIG
from contextlib import contextmanager

MYSQL_DATABASE_URL = URL.create(
    "mysql+pymysql",
    username=CONFIG.DB_MYSQL_USER,
    password=CONFIG.DB_MYSQL_PASSWORD,
    host=CONFIG.DB_MYSQL_HOST,
    port=CONFIG.DB_MYSQL_PORT,
    database=CONFIG.DB_MYSQL_DATABASE,
)

engine = create_engine(
    MYSQL_DATABASE_URL,
    # connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def sql_connection():
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
