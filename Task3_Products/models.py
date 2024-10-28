from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, \
    CheckConstraint, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    # Relationship to Product model
    products = relationship("Product", back_populates="category",
                            cascade="all, delete-orphan")

    # Self-referential relationship for nested categories
    parent = relationship("Category", remote_side=id,
                          backref="subcategories")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    # Adding check constraints for price and quantity
    __table_args__ = (
        CheckConstraint('price > 0', name='check_positive_price'),
        CheckConstraint('quantity >= 0', name='check_non_negative_quantity'),
    )

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(),
                        nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to Category model
    category = relationship("Category", back_populates="products")