from typing import Optional, Literal

from sqlalchemy import select, asc, desc
from fastapi import HTTPException
from sqlalchemy.orm import Session

from Task3_Products import models, schemas


def create_category(category_data: schemas.CategoryCreate, db: Session) -> models.Category:
    category_already_exist = db.query(models.Category).filter(models.Category.name == category_data.name).first()
    if category_already_exist:
        raise HTTPException(status_code=400, detail="Category already exists")

    if category_data.parent_id:
        parent_category = db.query(models.Category).filter_by(id=category_data.parent_id).first()
        if not parent_category:
            raise HTTPException(status_code=404, detail="Parent category not found")

    category = models.Category(name=category_data.name, parent_id=category_data.parent_id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_categories(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        sort_by: Literal["id", "name"] = None,
        sort_order: Literal["asc", "desc"] = None,
) -> list[models.Category]:

    query = db.query(models.Category)

    if sort_by:
        if sort_by == "id":
            order = asc(models.Category.id) if sort_order == "asc" else desc(
                models.Category.id)
        elif sort_by == "name":
            order = asc(
                models.Category.name) if sort_order == "asc" else desc(
                models.Category.name)
        else:
            raise HTTPException(status_code=400,
                                detail="Invalid sort_by field")

        query = query.order_by(order)

    query = query.offset(skip).limit(limit)
    return query.all()


def get_category_by_id(category_id: int, db: Session) -> Optional[models.Category]:
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


def update_category(category_id: int, category_data: schemas.CategoryUpdate, db: Session) -> models.Category:
    category = get_category_by_id(category_id=category_id, db=db)
    if category_data.name:
        category.name = category_data.name
    if category_data.parent_id:
        parent_category = db.query(models.Category).filter_by(id=category_data.parent_id).first()
        if not parent_category:
            raise HTTPException(status_code=404, detail="Parent category not found")
        category.parent_id = category_data.parent_id

    db.commit()
    db.refresh(category)
    return category


def delete_category(category_id: int, db: Session) -> None:
    category = get_category_by_id(db=db, category_id=category_id)

    db.delete(category)
    db.commit()
    return None
