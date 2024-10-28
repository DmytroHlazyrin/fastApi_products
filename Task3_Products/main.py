from fastapi import FastAPI

from Task3_Products import models
from Task3_Products.database import engine
from Task3_Products.routers import categories

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shop")

app.include_router(categories.router, tags=["Categories"])
