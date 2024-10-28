import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from Task3_Products.config import DATABASE_URL


engine = create_engine(DATABASE_URL, echo=True)
session_maker = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)


# def get_session() -> Generator[Session]:
#     with session_maker() as session:
#         yield session


def get_db() -> Session:
    db = session_maker()
    try:
        yield db
    finally:
        db.close()
