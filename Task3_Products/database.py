from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from Task3_Products.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)
session_maker = sessionmaker(
    bind=engine, class_=Session, expire_on_commit=False
)


def get_db() -> Session:
    db = session_maker()
    try:
        yield db
    finally:
        db.close()
