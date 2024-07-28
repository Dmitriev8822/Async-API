# schemas.py

from typing import List, Optional
from pydantic import BaseModel


# === Schemas for Categories ===

class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode: True


# === Schemas for Products ===

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode: True


# === Schemas for Orders ===

class OrderBase(BaseModel):
    customer_id: int
    product_id: int
    quantity: int


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    total_price: float

    class Config:
        orm_mode: True


# === Schemas for Customers ===

class CustomerBase(BaseModel):
    username: str
    password: str


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class Customer(CustomerBase):
    pass

    class Config:
        orm_mode: True
