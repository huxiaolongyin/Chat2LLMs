from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from core.config import CONFIG
from contextlib import contextmanager

MYSQL_DATABASE_URL = URL.create(
    "mysql+pymysql",
    username=CONFIG.MYSQL_USER,
    password=CONFIG.MYSQL_PASSWORD,
    host=CONFIG.MYSQL_HOST,
    port=CONFIG.MYSQL_PORT,
    database=CONFIG.MYSQL_DATABASE,
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
