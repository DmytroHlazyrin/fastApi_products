import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

from Task3_Products import models
from Task3_Products.database import get_db
from Task3_Products.main import app
from Task3_Products.models import Base
from logger import setup_logger

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(autouse=True)
def disable_logging():
    logger = setup_logger("Shop", "shop.log")
    logger.disabled = True
    yield
    logger.disabled = False


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture()
def initial_data() -> dict:
    categories = []
    products = []

    for i in range(10):
        category = {"name": f"Category {i + 1}"}
        categories.append(category)

        for j in range(2):
            product = {
                "name": f"Product {i + 1}-{j + 1}",
                "description": f"Description for product {i + 1}-{j + 1}",
                "price": 10.0 * (i + 1),
                "quantity": 100 * (i + 1),
                "category_id": i + 1
            }
            products.append(product)

    return {"categories": categories, "products": products}

@pytest.fixture(scope="function")
def init_data(db: Session, initial_data):
    for category in initial_data["categories"]:
        cat = models.Category(**category)
        db.add(cat)
    db.commit()

    for product in initial_data["products"]:
        prod = models.Product(**product)
        db.add(prod)
    db.commit()

    return initial_data["categories"], initial_data["products"]
