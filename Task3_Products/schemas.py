from datetime import datetime
from typing import Optional

from pydantic import BaseModel, conint, condecimal


class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None


class Category(CategoryBase):
    id: int


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: condecimal(gt=0, decimal_places=2)
    quantity: conint(ge=0)
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[condecimal(gt=0, decimal_places=2)] = None
    quantity: Optional[conint(ge=0)] = None
    category_id: Optional[int] = None


class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
