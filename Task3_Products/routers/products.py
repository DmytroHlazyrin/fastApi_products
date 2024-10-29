from typing import Literal, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from Task3_Products import crud, schemas, database


router = APIRouter()


@router.post(
    "/products/",
    response_model=schemas.Product,
    status_code=201
)
async def create_product_endpoint(
    product_data: schemas.ProductCreate,
    db: Session = Depends(database.get_db)
) -> schemas.Product:
    """Create a new product."""
    return crud.create_product(product_data=product_data, db=db)


@router.get("/products/", response_model=list[schemas.Product])
def read_products_endpoint(
    category_id: Optional[int] = None,
    skip: Optional[int] = 0,
    limit: Optional[int] = 10,
    sort_by: Literal["id", "name", "price"] = "id",
    sort_order: Literal["asc", "desc"] = "asc",
    db: Session = Depends(database.get_db)
) -> list[schemas.Product]:
    """Read products."""
    return crud.get_products(
        db=db,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
        category_id=category_id
    )


@router.get("/products/{product_id}", response_model=schemas.Product)
def read_product_endpoint(
        product_id: int,
        db: Session = Depends(database.get_db)
) -> schemas.Product:
    """Retrieve a single product."""
    return crud.get_product_by_id(product_id=product_id, db=db)


@router.patch("/products/{product_id}", response_model=schemas.Product)
async def update_product_endpoint(
    product_id: int,
    product_data: schemas.ProductUpdate,
    db: Session = Depends(database.get_db)
) -> schemas.Product:
    """Update a single product."""
    return crud.update_product(
        product_id=product_id,
        product_data=product_data,
        db=db
    )


@router.delete("/products/{product_id}", status_code=204)
async def delete_product_endpoint(
    product_id: int,
    db: Session = Depends(database.get_db)
) -> None:
    """Delete a single product."""
    return crud.delete_product(product_id=product_id, db=db)
