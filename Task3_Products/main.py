from fastapi import FastAPI
from Task3_Products.routers import categories, products

app = FastAPI(title="Shop")

app.include_router(categories.router, tags=["Categories"])

app.include_router(products.router, tags=["Products"])
