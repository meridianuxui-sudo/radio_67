from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.core.config import get_settings

def _engine():
    url = get_settings().database_url
    return create_engine(url, connect_args={"check_same_thread": False} if url.startswith("sqlite") else {})
engine = _engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
class Base(DeclarativeBase): pass
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
