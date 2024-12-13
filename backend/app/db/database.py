from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent 
DB_FILE = 'app/sql_app.db'
DATABASE_URL = f"sqlite:///{BASE_DIR / DB_FILE}"

logger.info(f"Database BASE_DIR: {BASE_DIR}")
logger.info(f"Full database path: {BASE_DIR / DB_FILE}")

# Create directory if it doesn't exist
db_path = Path(DATABASE_URL.replace('sqlite:///', ''))
db_dir = db_path.parent
db_dir.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Log database connection info
def log_db_info():
    db_path = Path(DATABASE_URL.replace('sqlite:///', ''))
    logger.info(f"Database file exists: {db_path.exists()}")
    if db_path.exists():
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Available tables: {tables}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:  # noqa: E722
        db.rollback()
        raise
    else:
        if db.is_active:
            db.commit()
    finally:
        db.close()

# Log info after setup
log_db_info()