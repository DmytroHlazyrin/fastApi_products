from typing import Literal, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from Task3_Products import crud, models, schemas
from Task3_Products.crud import get_category_by_id
from Task3_Products.database import get_db

router = APIRouter()

@router.post("/categories/", response_model=schemas.Category, status_code=201)
async def create_category_endpoint(
    category_data: schemas.CategoryCreate,
    db: Session = Depends(get_db)
) -> models.Category:
    """Create a new author."""
    return crud.create_category(category_data=category_data, db=db)



@router.get("/categories/", response_model=list[schemas.Category])
async def read_categories(
    skip: Optional[int] = 0,
    limit: Optional[int] = 10,
    sort_by: Literal["id", "name"] = None,
    sort_order: Literal["asc", "desc"] = None,
    db: Session = Depends(get_db)
) -> list[models.Category]:
    """Retrieve a list of categories."""
    return crud.get_categories(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order, db=db)


@router.get("/categories/{category_id}", response_model=schemas.Category)
async def read_category(
    category_id: int,
    db: Session = Depends(get_db)
) -> models.Category:
    """Retrieve a single category."""
    return get_category_by_id(category_id=category_id, db=db)


@router.patch("/categories/{category_id}", response_model=schemas.Category)
async def update_category(
    category_id: int,
    category_data: schemas.CategoryUpdate,
    db: Session = Depends(get_db)
) -> models.Category:
    """Update a single category."""
    return crud.update_category(category_id=category_id, category_data=category_data, db=db)


@router.delete("/categories/{category_id}", status_code=204)
async def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """Delete a single category."""
    return crud.delete_category(category_id=category_id, db=db)
