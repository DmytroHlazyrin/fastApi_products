from typing import Optional, Literal

from sqlalchemy import asc, desc
from fastapi import HTTPException
from sqlalchemy.orm import Session

from Task3_Products import models, schemas
from logger import setup_logger

logger = setup_logger("Shop", "shop.log")


def create_category(category_data: schemas.CategoryCreate, db: Session) -> models.Category:
    category_already_exist = db.query(models.Category).filter(models.Category.name == category_data.name).first()
    if category_already_exist:
        raise HTTPException(status_code=400, detail="Category already exists")

    if category_data.parent_id:
        parent_category = db.query(models.Category).filter(
            models.Category.id == category_data.parent_id).first()
        if not parent_category:
            raise HTTPException(status_code=404, detail="Parent category not found")
    else:
        category_data.parent_id = None

    category = models.Category(name=category_data.name, parent_id=category_data.parent_id)
    db.add(category)
    db.commit()
    db.refresh(category)
    logger.info(f"Category '{category.name}' created")
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
    logger.info(f"Category '{category.name}' updated")
    return category


def delete_category(category_id: int, db: Session) -> None:
    category = get_category_by_id(db=db, category_id=category_id)

    db.delete(category)
    db.commit()
    logger.info(f"Category '{category.name}' deleted")
    return None


def create_product(product_data: schemas.ProductCreate, db: Session) -> models.Product:
    get_category_by_id(category_id=product_data.category_id, db=db)

    product_already_exist = db.query(models.Product).filter(models.Product.name == product_data.name).first()
    if product_already_exist:
        raise HTTPException(status_code=400, detail="Product already exists")


    product = models.Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        quantity=product_data.quantity,
        category_id=product_data.category_id
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    logger.info(f"Product '{product.name}' created")
    return product

def get_products(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        sort_by: Literal["id", "name", "price"] = None,
        sort_order: Literal["asc", "desc"] = None,
        category_id: Optional[int] = None,
) -> list[models.Product]:



    query = db.query(models.Product)

    if category_id:
        get_category_by_id(category_id=category_id, db=db)
        query = query.filter(models.Product.category_id == category_id)

    if sort_by:
        if sort_by == "id":
            order = asc(models.Product.id) if sort_order == "asc" else desc(
                models.Product.id)
        elif sort_by == "name":
            order = asc(
                models.Product.name) if sort_order == "asc" else desc(
                models.Product.name)
        elif sort_by == "price":
            order = asc(
                models.Product.price) if sort_order == "asc" else desc(
                models.Product.price)
        else:
            raise HTTPException(status_code=400,
                                detail="Invalid sort_by field")

        query = query.order_by(order)

    query = query.offset(skip).limit(limit)
    return query.all()


def get_product_by_id(product_id: int, db: Session) -> Optional[models.Product]:
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


def update_product(product_id: int, product_data: schemas.ProductUpdate, db: Session) -> models.Product:
    product = get_product_by_id(product_id=product_id, db=db)

    if product_data.name:
        product.name = product_data.name
    if product_data.description:
        product.description = product_data.description
    if product_data.price:
        product.price = product_data.price
    if product_data.quantity:
        product.quantity = product_data.quantity
    if product_data.category_id:
        get_category_by_id(category_id=product_data.category_id, db=db)
        product.category_id = product_data.category_id

    db.commit()
    db.refresh(product)
    logger.info(f"Product '{product.name}' updated")
    return product


def delete_product(product_id: int, db: Session) -> None:
    product = get_product_by_id(db=db, product_id=product_id)
    db.delete(product)
    db.commit()
    logger.info(f"Product '{product.name}' deleted")
    return None
